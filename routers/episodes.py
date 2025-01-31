from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy import text

from config import db_manager
from models.episodes import TimeOfDay
from schemas.episodes import EpisodeCreate, EpisodeResponse, EpisodeUpdate

api_router = APIRouter()
get_db = db_manager.get_db
execute = db_manager.execute

@api_router.post("/", response_model=EpisodeResponse)
def create_episode(episode: EpisodeCreate):
    if isinstance(episode.time_of_day, TimeOfDay):
        episode.time_of_day = episode.time_of_day.value
    query = text("INSERT INTO episodes (title, description, duration, audio_link, is_bookmark, is_deleted, time_of_day) VALUES (:title, :description, :duration, :audio_link, :is_bookmark, :is_deleted, :time_of_day) RETURNING *")
    new_episode = execute(query, params=episode.model_dump())
    return new_episode

@api_router.get("/{episode_id}", response_model=EpisodeResponse)
def get_episode(episode_id: int):
    query = text("SELECT * FROM episodes WHERE id = :episode_id")
    episodes = execute(query, params={"episode_id": episode_id})
    if len(episodes) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Episode not found")
    return episodes[0]

@api_router.get("/", response_model=list[EpisodeResponse])
def list_episodes(
    is_bookmark: bool = Query(None, description="Filter by bookmark status"),
    time_of_day: TimeOfDay = Query(None, description="Filter by time of day")
):
    # Start building the query
    query = "SELECT * FROM episodes WHERE 1=1 AND is_deleted=false"
    
    # Add filter for is_bookmark if provided
    if is_bookmark is not None:
        query = query + f" AND is_bookmark = :is_bookmark"
    
    # Add filter for time_of_day if provided
    if time_of_day is not None:
        query = query + f" AND time_of_day = :time_of_day"
    
    time_of_day_str = None
    if time_of_day is not None:
        if isinstance(time_of_day, TimeOfDay):
            time_of_day_str = time_of_day.value
        else:
            time_of_day_str = time_of_day

    # Execute the query with the filters applied
    res = execute(text(query), {"is_bookmark": is_bookmark, "time_of_day": time_of_day_str})
    
    return res

@api_router.put("/{episode_id}", response_model=EpisodeResponse)
def update_episode(episode_id: int, episode: EpisodeUpdate):
    query = text("SELECT * FROM episodes WHERE id = :episode_id")
    existing_episodes = execute(query, params={"episode_id": episode_id})
    if not existing_episodes or len(existing_episodes) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Episode not found")
    existing_episode = existing_episodes[0]
    print("existing_episode:", existing_episode)
    print("episode update: ", episode.model_dump())
    for key, value in episode.model_dump().items():
        if value is not None:
            existing_episode[key] = value

    print("Existing episode Changes:", existing_episode)
    query = text("UPDATE episodes SET title = :title, description = :description, duration = :duration, audio_link = :audio_link, is_bookmark = :is_bookmark, is_deleted = :is_deleted WHERE id = :id")
    execute(query, params=existing_episode)

    return existing_episode

@api_router.delete("/{episode_id}")
def delete_episode(episode_id: int):
    query = text("SELECT * FROM episodes WHERE id = :episode_id")
    existing_episodes = execute(query, params={"episode_id": episode_id})
    if not existing_episodes and len(existing_episodes) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Episode not found")
    # existing_episode = existing_episodes[0]
    query = text("DELETE FROM episodes WHERE id = :episode_id")
    execute(query, params={"episode_id": episode_id})
    return {"detail": "Episode deleted successfully"}