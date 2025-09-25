def resumePrompt(text: str):
    return f"""
Ты получаешь текст резюме:

{text}

Задача:
1. Проанализируй резюме и выдели данные строго из текста.
2. Верни результат строго в формате **валидного JSON** по следующей структуре:

{{
  "profile": {{
    "first_name": "",
    "last_name": "",
    "middle_name": "",
    "birth_date": "YYYY-MM-DD",
    "location": "",
    "address": "",
    "gender": "male/female/unspecified",
    "summary": "",
    "industry":"it/education/healthcare/construction/finance&accounting/production/logistics&transport/marketing&ads/agricultural/tourism&hotels/public_service/other"
    "links": [
      {{ "url": "", "type": "github/linkedin/facebook/x/instagram/email/phone/other" }}
    ]
  }},
  "skills": [
    {{ "name": ""}}
  ],
  "education": [
    {{
      "institution": "",
      "degree": "",
      "field_of_study": "",
      "start_year": "YYYY",
      "end_year": "YYYY",
      "description": ""
    }}
  ],
  "experiences": [
    {{
      "job_title": "",
      "company_name": "",
      "company_address": "",
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD",
      "is_current": false,
      "description": ""
    }}
  ],
  "languages": [
    {{
      "name": "",
      "language_proficiency": "A1/A2/B1/B2/C1/C2/native"
    }}
  ]
}}

Правила:
- Извлекай только те данные, которые реально есть в тексте.
- Если в резюме встречаются негативные или неподтверждённые данные (например: "ленивый", "нет опыта", "плохой английский", "слабые навыки"), то такие данные не включай в JSON.
- Не добавляй выдуманных или несоответствующих данных.
- Если информации нет — используй пустые строки "" или пустые массивы [].
- Даты строго в формате: "YYYY" или "YYYY-MM-DD".
- Верни только JSON (без текста, пояснений или комментариев).
- JSON должен быть валидным (валидируется без ошибок).
"""
# ,
#   "additions": [
#     {{
#       "title": "",
#       "description": "",
#       "category": "project/certificate/resume/portfolio/achievement/diploma",
#       "links": [
#         {{ "url": "", "type": "github/linkedin/facebook/x/instagram/email/phone/other" }}
#       ]
#     }}
#   ]