from datetime import datetime, timedelta
import pytz # type: ignore

from sqlalchemy import text

from config import db_manager
from helpers.tts import convert_text_to_speech
from models.episodes import TimeOfDay
# from proj.helper import get_current_date_ist, get_time_of_day
from schemas.episodes import EpisodeCreate
from schemas.text_to_speech import TextToSpeechRegisterRequest

execute = db_manager.execute

def get_time_of_day() -> TimeOfDay:
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist).time()

    if now >= datetime.strptime("08:00", "%H:%M").time() and now <= datetime.strptime("18:00", "%H:%M").time():
        return TimeOfDay.MORNING
    return TimeOfDay.ENDOFDAY

def get_current_date_ist() -> str:
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    return now.strftime("%d %b, %Y")

def get_week_range_ist() -> tuple:
    ist = pytz.timezone("Asia/Kolkata")
    today = datetime.now(ist).date()
    
    # Find the Monday of the current week
    week1 = today - timedelta(days=today.weekday())  # Monday of this week
    # Find the Sunday of the current week
    week2 = week1 + timedelta(days=6)  # Sunday of this week
    
    return week1.strftime("%d %b"), week2.strftime("%d %b")

def generate_episode(summary: str, is_weekly: bool, time: str):
    try:
        body = TextToSpeechRegisterRequest(text=summary)
        response = convert_text_to_speech(body)
    except Exception as exc:
        print(f"Error in converting text to speech - {body}")
        raise Exception(str(exc))

    audio_link = response["s3_url"]

    title, time_of_day = None, None
    if is_weekly:
        time_of_day = TimeOfDay.ENDOFWEEK
        title = f"Weekly Recap"
    else:
        time_of_day = TimeOfDay.MORNING if time == "morning" else TimeOfDay.ENDOFDAY
        current_date = get_current_date_ist()

        if time_of_day == TimeOfDay.MORNING:
            title = f"Start Your Day: Morning Insights"
        else:
            title = f"End of Day Recap"
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    # create an episode
    episode = EpisodeCreate(
        title=title,
        description=summary,
        duration=response["audio_duration"],
        audio_link=audio_link,
        is_bookmark=False,
        is_deleted=False,
        time_of_day=time_of_day.value,
        published_at=now,
    )

    query = text("INSERT INTO episodes (title, description, duration, audio_link, is_bookmark, is_deleted, time_of_day) VALUES (:title, :description, :duration, :audio_link, :is_bookmark, :is_deleted, :time_of_day) RETURNING *")
    new_episode = execute(query, params=episode.model_dump())