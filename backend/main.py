from fastapi import FastAPI

from backend.uploads import router as upload_router
from backend.extraction_router import router as extraction_router


app = FastAPI(
    title="VERIQO",
    description="AI-powered document trust and verification",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(extraction_router)


@app.get("/")
def root():
    return {
        "message": "VERIQO backend is running",
        "status": "online"
    }