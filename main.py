from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from config import cfg
from routers import episodes
from routers import celery_task_run

if not cfg.project_name:
    cfg.project_name = "AudioByte"

app = FastAPI(
    title=cfg.project_name,
    debug=True,
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

allowed_origins = [
    "http://localhost:1234",  # Your frontend URL
    "http://51.21.128.134:4000",  # Optional: Add other allowed origins if needed
    "*",  # You can use "*" to allow all origins (not recommended for production)
]

# Enable CORS for all origins on WebSocket routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

app.include_router(
    episodes.api_router,
    prefix="/episodes",
    tags=["AudioByte Api's"]
)

app.include_router(
    celery_task_run.api_router,
    prefix="/tasks",
    tags=["AudioByte Api's"]
)


@app.get("/", response_class=HTMLResponse)
def read_root():
    html = open("static/index.html", "r").read()
    return html
