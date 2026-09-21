from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import Message
from app.routers.message import router as message_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Message Classifier API",
    description="API for classifying and analyzing business messages using AI",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Message routes
app.include_router(message_router)


# Health check
@app.get("/api/health")
def health_check():
    return {
        "status": "ok"
    }