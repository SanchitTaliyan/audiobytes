from fastapi import APIRouter, status
from pydantic import BaseModel
from proj.tasks import create_morning_episode, create_eod_episode, create_weekly_episode

api_router = APIRouter()

class EpisodeData(BaseModel):
    leads_received: int
    fu_completed: int
    planned_sv: int
    planned_fu: int
    planned_f2f: int
    total_bookings: int
    bookings_done: int
    bookings_at_l1: int
    bookings_at_l2: int
    planned_sv_leads: list[str]
    planned_f2f_leads: list[str]
    planned_fu_leads: list[str]
    booking_at_l1_leads: list[str]
    booking_at_l2_leads: list[str]

@api_router.post("/run/morning-episode", status_code=status.HTTP_202_ACCEPTED)
def run_morning_episode(data: EpisodeData):
    result = create_morning_episode(data.model_dump())  # Use model_dump() here
    return {"message": "Morning episode task completed", "result": result}

@api_router.post("/run/eod-episode", status_code=status.HTTP_202_ACCEPTED)
def run_eod_episode(data: EpisodeData):
    result = create_eod_episode(data.model_dump())  # Use model_dump() here
    return {"message": "EOD episode task completed", "result": result}

@api_router.post("/run/weekly-episode", status_code=status.HTTP_202_ACCEPTED)
def run_weekly_episode(data: EpisodeData):
    result = create_weekly_episode(data.model_dump())  # Use model_dump() here
    return {"message": "Weekly episode task completed", "result": result}
