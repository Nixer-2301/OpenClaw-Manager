import os
import sys
import threading
import webbrowser
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

# PyInstaller extracts files to sys._MEIPASS
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).parent

sys.path.insert(0, str(BASE_DIR / "python-backend"))

from api.skills import router as skills_router
from api.models import router as models_router
from api.plugins import router as plugins_router
from api.process import router as process_router
from api.config import router as config_router
from api.logs import router as logs_router
from api.stats import router as stats_router
from api.settings import router as settings_router
from api.sessions import router as sessions_router

app = FastAPI(title="OpenClaw Manager API", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(skills_router, prefix="/api/skills", tags=["Skills"])
app.include_router(models_router, prefix="/api/models", tags=["Models"])
app.include_router(plugins_router, prefix="/api/plugins", tags=["Plugins"])
app.include_router(process_router, prefix="/api/process", tags=["Process"])
app.include_router(config_router, prefix="/api/config", tags=["Config"])
app.include_router(logs_router, prefix="/api/logs", tags=["Logs"])
app.include_router(stats_router, prefix="/api/stats", tags=["Stats"])
app.include_router(settings_router, prefix="/api/settings", tags=["Settings"])
app.include_router(sessions_router, prefix="/api/sessions", tags=["Sessions"])


@app.get("/api/health")
async def health():
    return {"status": "healthy"}


@app.get("/", response_class=HTMLResponse)
async def index():
    index_file = BASE_DIR / "dist" / "index.html"
    if index_file.exists():
        return index_file.read_text(encoding="utf-8")
    return "<html><body><h1>OpenClaw Manager</h1><p>Frontend not found.</p></body></html>"


@app.get("/assets/{path:path}")
async def assets(path: str):
    file_path = BASE_DIR / "dist" / "assets" / path
    if file_path.exists():
        suffix = file_path.suffix.lower()
        media_types = {".js": "application/javascript", ".css": "text/css", ".svg": "image/svg+xml", ".png": "image/png"}
        media_type = media_types.get(suffix, "application/octet-stream")
        return FileResponse(str(file_path), media_type=media_type)
    return FileResponse(str(BASE_DIR / "dist" / "index.html"))


@app.get("/{path:path}")
async def catch_all(path: str):
    # Check if it matches static assets
    file_path = BASE_DIR / "dist" / path
    if file_path.exists() and file_path.is_file():
        suffix = file_path.suffix.lower()
        media_types = {".js": "application/javascript", ".css": "text/css", ".svg": "image/svg+xml", ".png": "image/png"}
        media_type = media_types.get(suffix, "application/octet-stream")
        return FileResponse(str(file_path), media_type=media_type)
    # SPA fallback - return index.html for all non-API routes
    return FileResponse(str(BASE_DIR / "dist" / "index.html"))


def open_browser():
    webbrowser.open("http://127.0.0.1:8000")


def main():
    host = "127.0.0.1"
    port = 8000

    threading.Timer(1.5, open_browser).start()

    print(f"OpenClaw Manager v1.2.0  http://{host}:{port}")
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        log_config={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(levelprefix)s %(message)s",
                    "use_colors": False,
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "uvicorn": {"handlers": ["default"], "level": "INFO"},
                "uvicorn.error": {"level": "INFO"},
            },
        },
    )


if __name__ == "__main__":
    main()
