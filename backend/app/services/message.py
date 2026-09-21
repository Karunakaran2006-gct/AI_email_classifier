from sqlalchemy.orm import Session

from app.models.message import Message
from app.repositories.message import create_message, get_messages
from app.schemas.message import MessageCreate


def create_message_service(
    db: Session,
    message_data: MessageCreate
) -> Message:

    message = Message(
        sender=message_data.sender,
        subject=message_data.subject,
        body=message_data.body
    )

    return create_message(db, message)


def get_messages_service(db: Session) -> list[Message]:
    return get_messages(db)