from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_current_admin
from app.schemas.contact import ContactInfoUpdate
from app.services import contact_service


router = APIRouter(
    prefix="/api/contact",
    tags=["Contact"]
)


@router.get("/")
async def get_contact_info():
    contact = await contact_service.get_contact_info()

    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact section not found."
        )

    return contact


@router.patch("/")
async def update_contact_info(
    contact_data: ContactInfoUpdate,
    admin_id: str = Depends(get_current_admin)
):
    update_data = contact_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update."
        )

    updated = await contact_service.update_contact_info(
        update_data
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Contact section not found."
        )

    contact = await contact_service.get_contact_info(
    is_published=None
)

    return {
        "message": "Contact information updated successfully",
        "contact": contact
    }