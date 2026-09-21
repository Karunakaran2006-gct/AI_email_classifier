from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.message import MessageCreate
from app.services.message import create_message_service

router = APIRouter(prefix="/api/messages", tags=["Messages"])


@router.post("/")
def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    return create_message_service(db, message)