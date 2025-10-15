import asyncio
import os
from PyPDF2 import PdfReader
import docx2txt
import pytesseract
from PIL import Image
import cv2
import numpy as np
import tempfile
from fastapi import File, UploadFile

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

tessdata_dir = r"C:\Program Files\Tesseract-OCR\tessdata"
langs = [f.replace(".traineddata", "") for f in os.listdir(tessdata_dir) if f.endswith(".traineddata")]
langs_str = "+".join(langs) if langs else "eng"  # fallback на eng


def preprocess_image(image_path):
    try:
        image = cv2.imread(image_path)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        return thresh
    except Exception as e:
        return f"Ошибка: {str(e)}"


async def extractText(file: UploadFile = File(...)):
    filename = file.filename
    ext = filename.split(".")[-1].lower()

    content = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    text = ""
    try:
        if ext == "txt":
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        elif ext == "pdf":
            reader = await asyncio.to_thread(PdfReader, tmp_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif ext in ["docx", "doc"]:
            text = await asyncio.to_thread(docx2txt.process, tmp_path)
        elif ext in ["jpg", "jpeg", "png"]:
            enhanced_img = await asyncio.to_thread(preprocess_image, tmp_path)
            pil_img = Image.fromarray(enhanced_img)
            pil_img.show()
            custom_config = r'--oem 3 --psm 6'
            text = await asyncio.to_thread(pytesseract.image_to_string, pil_img, lang=langs_str,config=custom_config)
        else:
            return {'error': "Неподдерживаемый формат файла"}
    except Exception as e:
        return {'error': f"Ошибка обработки файла: {str(e)}"}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    print(text)
    return {'text': text}