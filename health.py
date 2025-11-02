from fastapi import APIRouter
import os, platform, datetime

router = APIRouter()

@router.get("/healthz")
def health_check():
    return {
        "status": "✅ OK",
        "time": datetime.datetime.now().isoformat(),
        "python_version": platform.python_version(),
        "os": platform.system(),
        "env": {
            "ENVIRONMENT": os.getenv("ENVIRONMENT"),
            "DEBUG": os.getenv("DEBUG"),
            "PORT": os.getenv("PORT"),
        }
    }
