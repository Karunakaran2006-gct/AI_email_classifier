from sqlalchemy.orm import Session

from app.models.message import Message


def create_message(db: Session, message: Message) -> Message:
    db.add(message)
    db.commit()
    db.refresh(message)

    return message