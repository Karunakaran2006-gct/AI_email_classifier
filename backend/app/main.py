from fastapi import FastAPI

from app.database import Base, engine
from app.models import Message
from app.routers.message import router as message_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(message_router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}