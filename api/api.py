from google import genai
import json
from fastapi.responses import JSONResponse
from .prompts import resumePrompt

client = genai.Client(api_key="AIzaSyDMIL5X0R_YEt8a0jzvi0lNHXFnK7Y7JTM")
model_name = "gemini-2.0-flash"


def resumeCorrect(text: str):
    try:
        # Генерация контента через API
        response = client.models.generate_content(
            model=model_name, contents=resumePrompt(text)
        )
        # Пробуем распарсить JSON (обрезаем лишние символы если нужно)
        try:
            result_json = json.loads(response.text[8:-3])
        except json.JSONDecodeError:
            return {"error": "AI response is not valid JSON", "raw": response.text}
        print(result_json)
        return {"response": result_json}
    
    except Exception as e:
        # Ловим любые ошибки (сеть, API, таймауты)
        return {"error": f"Failed to process resume: {str(e)}"}
