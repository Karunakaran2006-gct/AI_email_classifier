from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.message import MessageCreate
from app.services.message import (
    create_message_service,
    get_messages_service,
    get_message_by_id_service,
    delete_message_service,
    analyze_message_service,
    get_summary_service
)


router = APIRouter(
    prefix="/api/messages",
    tags=["Messages"]
)


@router.post("/")
def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    return create_message_service(db, message)


@router.get("/")
def get_messages(
    search: str | None = None,
    category: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db)
):
    return get_messages_service(
        db,
        search=search,
        category=category,
        priority=priority
    )

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db)
):
    return get_summary_service(db)


@router.get("/{message_id}")
def get_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    message = get_message_by_id_service(db, message_id)

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    return message


@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_message_service(db, message_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    return {
        "message": "Message deleted successfully"
    }


@router.post("/{message_id}/analyze")
def analyze_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    message = analyze_message_service(db, message_id)

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    return message