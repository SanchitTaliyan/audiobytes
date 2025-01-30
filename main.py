from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from config import cfg
from routers import podcast

if not cfg.project_name:
    cfg.project_name = "AudioByte"

app = FastAPI(
    title=cfg.project_name,
    debug=True,
)

allowed_origins: list[str] = []
allowed_origin_regex = r"https?://([a-zA-Z0-9-]+\.)*audiobyte\.com"

# Enable CORS for all origins on WebSocket routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=allowed_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

app.include_router(podcast.api_router, prefix="/podcasts", tags=["AudioByte Api's"])

@app.get("/")
def read_root():
    return {"message": "Hello World!"}