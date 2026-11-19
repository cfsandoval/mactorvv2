import sys
from pathlib import Path

# Add project root and backend folder to sys.path for Vercel serverless environment
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "backend"))

from backend.app import app

# Health check route for Vercel deployment verification
@app.get("/api/health")
def vercel_health():
    return {
        "status": "healthy",
        "environment": "Vercel Serverless",
        "service": "MACTOR PROSP Engine"
    }
