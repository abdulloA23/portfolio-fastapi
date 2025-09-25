from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from extract import extractText
from api.api import resumeCorrect
from pydantic import BaseModel

from sentence_transformers import SentenceTransformer, util

app = FastAPI()

model = SentenceTransformer("all-MiniLM-L6-v2")

class VacancyItem(BaseModel):
    id: int
    text: str


class CompareRequest(BaseModel):
    cv_id: int
    cv_text: str
    vacancies: List[VacancyItem]
    top_n: int = 5


@app.post("/match_vacancy")
def match(req: CompareRequest):
    cv_embedding = model.encode(req.cv_text, convert_to_tensor=True)
    
    vacancy_embeddings = model.encode([v.text for v in req.vacancies], convert_to_tensor=True)
    
    similarities = util.cos_sim(cv_embedding, vacancy_embeddings)[0]
    
    ranked = sorted(
        [{"vacancy_id": req.vacancies[i].id, "score": float(similarities[i])}
         for i in range(len(req.vacancies))],
        key=lambda x: x["score"], reverse=True
    )
    
    return {
        "cv_id": req.cv_id,
        "recommendations": ranked[:req.top_n]
    }


class ProfileItem(BaseModel):
    id: int
    text: str

class VacancyMatchRequest(BaseModel):
    vacancy_id: int
    vacancy_text: str
    profiles: List[ProfileItem]
    top_n: int = 5

@app.post("/match_user")
def match_vacancy(req: VacancyMatchRequest):
    vacancy_embedding = model.encode(req.vacancy_text, convert_to_tensor=True)

    profile_embeddings = model.encode([p.text for p in req.profiles], convert_to_tensor=True)

    similarities = util.cos_sim(vacancy_embedding, profile_embeddings)[0]

    ranked = sorted(
        [{"profile_id": req.profiles[i].id, "score": float(similarities[i])}
         for i in range(len(req.profiles))],    
        key=lambda x: x["score"], reverse=True
    )

    return {
        "vacancy_id": req.vacancy_id,
        "recommendations": ranked[:req.top_n]
    }


@app.post("/extract-text/")
async def extract(file: UploadFile = File(...)):
    text_result = await extractText(file)
    
    if 'error' in text_result:
        return JSONResponse({'error': text_result['error']}, status_code=500)
    
    text = text_result['text']
    
    result = resumeCorrect(text)
    
    if 'error' in result:
        return JSONResponse({'error': result['error'], 'raw': result.get('raw', '')}, status_code=500)
    return JSONResponse({'response': result['response']}, status_code=200)
