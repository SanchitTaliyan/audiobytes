from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from config import db_manager
from schemas.episodes import EpisodeCreate, EpisodeResponse, EpisodeUpdate

api_router = APIRouter()
get_db = db_manager.get_db
execute = db_manager.execute

@api_router.post("/", response_model=EpisodeResponse)
def create_episode(episode: EpisodeCreate, db: Session = Depends(get_db)):
    query = text("INSERT INTO episodes (title, description, duration, audio_link, is_bookmark, is_deleted) VALUES (:title, :description, :duration, :audio_link, :is_bookmark, :is_deleted) RETURNING *")
    new_episode = execute(query, params=episode.model_dump())
    return new_episode

@api_router.get("/{episode_id}", response_model=EpisodeResponse)
def get_episode(episode_id: int):
    query = text("SELECT * FROM episodes WHERE id = :episode_id")
    episode = execute(query, params={"episode_id": episode_id})
    if not episode:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Episode not found")
    return episode

@api_router.get("/", response_model=list[EpisodeResponse])
def list_episodes():
    query = text("SELECT * FROM episodes")
    res = execute(query)
    return res

@api_router.put("/{episode_id}", response_model=EpisodeResponse)
def update_episode(episode_id: int, episode: EpisodeUpdate, db: Session = Depends(get_db)):
    query = text("SELECT * FROM episodes WHERE id = :episode_id")
    existing_episode = execute(query, params={"episode_id": episode_id})
    if not existing_episode:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Episode not found")
    for key, value in episode.model_dump().items():
        setattr(existing_episode, key, value)
    query = text("UPDATE episodes SET title = :title, description = :description, duration = :duration, audio_link = :audio_link, is_bookmark = :is_bookmark, is_deleted = :is_deleted WHERE id = :episode_id")
    execute(query, params=episode.model_dump())
    return existing_episode

@api_router.delete("/{episode_id}")
def delete_episode(episode_id: int, db: Session = Depends(get_db)):
    query = text("SELECT * FROM episodes WHERE id = :episode_id")
    existing_episode = execute(query, params={"episode_id": episode_id})
    if not existing_episode:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Episode not found")
    query = text("DELETE FROM episodes WHERE id = :episode_id")
    execute(query, params={"episode_id": episode_id})
    return {"detail": "Episode deleted successfully"}