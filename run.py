import uvicorn

from config import cfg

if __name__ == "__main__":
    if not cfg.host:
        cfg.host = "0.0.0.0"
    uvicorn.run("main:app", host=cfg.host, port=cfg.port, reload=True)