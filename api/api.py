from google import genai
import json
import os
from fastapi.responses import JSONResponse
from .prompts import resumePrompt

# Используем переменную окружения
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)
model_name = "gemini-2.0-flash"


def resumeCorrect(text: str):
    try:
        response = client.models.generate_content(
            model=model_name, contents=resumePrompt(text)
        )
        try:
            result_json = json.loads(response.text[8:-3])
        except json.JSONDecodeError:
            return {"error": "AI response is not valid JSON", "raw": response.text}
        print(result_json)
        return {"response": result_json}
    
    except Exception as e:
        return {"error": f"Failed to process resume: {str(e)}"}