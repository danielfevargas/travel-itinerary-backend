from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from app.generator import generate_itinerary

app = FastAPI(title="Travel Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TravelPreferences(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: str
    traveler_type: str
    pace: str
    interests: List[str]
    budget_amount: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Travel Planner API funcionando ✅"}

@app.post("/generate")
async def generate(preferences: TravelPreferences):
    try:
        itinerary = generate_itinerary(preferences.dict())
        return itinerary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))