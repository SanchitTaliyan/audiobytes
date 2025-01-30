from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from config import db_manager
from models.episodes import Episode
from schemas.episodes import EpisodeCreate, EpisodeResponse, EpisodeUpdate

api_router = APIRouter()
get_db = db_manager.get_db

@api_router.post("/", response_model=EpisodeResponse)
def create_episode(episode: EpisodeCreate, db: Session = Depends(get_db)):
    new_episode = Episode(**episode.model_dump())
    db.add(new_episode)
    db.commit()
    db.refresh(new_episode)
    return new_episode

@api_router.get("/{episode_id}", response_model=EpisodeResponse)
def get_episode(episode_id: int, db: Session = Depends(get_db)):
    episode = db.query(Episode).filter(Episode.id == episode_id).first()
    if not episode:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Episode not found")
    return episode

@api_router.get("/", response_model=list[EpisodeResponse])
def list_episodes(db: Session = Depends(get_db)):
    return db.query(Episode).all()

@api_router.put("/{episode_id}", response_model=EpisodeResponse)
def update_episode(episode_id: int, episode: EpisodeUpdate, db: Session = Depends(get_db)):
    existing_episode = db.query(Episode).filter(Episode.id == episode_id).first()
    if not existing_episode:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Episode not found")
    for key, value in episode.model_dump().items():
        setattr(existing_episode, key, value)
    db.commit()
    db.refresh(existing_episode)
    return existing_episode

@api_router.delete("/{episode_id}")
def delete_episode(episode_id: int, db: Session = Depends(get_db)):
    episode = db.query(Episode).filter(Episode.id == episode_id).first()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    db.delete(episode)
    db.commit()
    return {"detail": "Episode deleted successfully"}