from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Preferences(BaseModel):
    likes: Optional[List[str]] = []
    dislikes: Optional[List[str]] = []
    notAllowed: Optional[List[str]] = []

class CustomWishes(BaseModel):
    daily: Optional[dict] = {}
    monday: Optional[dict] = {}
    friday: Optional[dict] = {}

class PatientParams(BaseModel):
    name: str
    category: int
    stage: int
    scheme: int
    week: List[int]
    calories: int
    preferences: Preferences
    customWishes: Optional[CustomWishes] = None
    fastingDays: Optional[List[str]] = []

@app.post("/build-week")
def build_week(data: PatientParams):
    days = []
    for i in range(1, 8):
        if i in [1, 5]:
            days.append(f"{i}-й день\n\nРД\n")
        else:
            days.append(f"""{i}-й день

Завтрак – творог 5% (150 г) с мёдом (10 г), киви (50 г), зелёный чай

Второй завтрак – яблоко 150 г

Обед – куриная грудка запечённая 150 г, гречка 100 г, салат из овощей с оливковым маслом

Ужин – тушёные овощи с индейкой 160 г, кефир 1% (200 мл)

""")
    additions = """
Добавления после 16.00
(в день можно выбрать 1 из разрешённых добавлений, до трёх раз в неделю, КРОМЕ 1 и 5-го дня)

• Горький шоколад 70% – 15 г.
• Зефир – 0.5 шт.
• Фрукты (цитрусовые, ягоды) – 100 г.
• Мёд – 15 г.
"""
    full_menu = "\n".join(days) + additions
    return {"weekMenu": full_menu}
