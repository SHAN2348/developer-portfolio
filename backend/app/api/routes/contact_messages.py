from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_admin
from app.schemas.contact_message import ContactMessageCreate
from app.services import contact_message_service


router = APIRouter(
    prefix="/api/contact-messages",
    tags=["Contact Messages"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def submit_contact_message(message_data: ContactMessageCreate):
    created_message = await contact_message_service.create_message(
        message_data.model_dump()
    )

    if created_message is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to submit contact message."
        )

    return {
        "message": "Your message has been sent successfully.",
        "contact_message": created_message
    }


@router.get("/admin")
async def get_all_messages(
    admin_id: str = Depends(get_current_admin)
):
    messages = await contact_message_service.get_all_messages()

    return {
        "total_messages": len(messages),
        "messages": messages
    }


@router.patch("/{message_id}/read")
async def mark_message_as_read(
    message_id: str,
    admin_id: str = Depends(get_current_admin)
):
    updated = await contact_message_service.mark_message_as_read(
        message_id
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Contact message not found."
        )

    return {
        "message": "Contact message marked as read."
    }


@router.delete("/{message_id}")
async def delete_contact_message(
    message_id: str,
    admin_id: str = Depends(get_current_admin)
):
    deleted = await contact_message_service.delete_message(
        message_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Contact message not found."
        )

    return {
        "message": "Contact message deleted successfully.",
        "message_id": message_id
    }