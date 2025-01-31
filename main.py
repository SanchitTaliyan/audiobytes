from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from config import cfg
from routers import episodes

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

allowed_origins: list[str] = []
# allowed_origin_regex = r"https?://([a-zA-Z0-9-]+\.)*audiobyte\.com"
allowed_origin_regex = r"*"

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

app.include_router(
    episodes.api_router,
    prefix="/episodes",
    tags=["AudioByte Api's"]
)


@app.get("/", response_class=HTMLResponse)
def read_root():
    html = open("static/index.html", "r").read()
    return html
