from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from app.core.dependencies import get_current_admin

from app.schemas.experience import (
    ExperienceCreate,
    ExperienceUpdate
)

from app.services import experience_service


router = APIRouter(
    prefix="/api/experience",
    tags=["Experience"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create_new_experience(
    experience: ExperienceCreate,
    admin_id: str = Depends(get_current_admin)
):
    experience_data = experience.model_dump()

    created_experience = await experience_service.create_experience(
        experience_data
    )

    if created_experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience section not found. Create it first."
        )

    return {
        "message": "Experience record created successfully",
        "experience": created_experience
    }

@router.get("/")
async def get_experiences():
    experiences = await experience_service.get_all_experiences()

    return {
        "total_experiences": len(experiences),
        "experiences": experiences
    }

@router.get("/admin")
async def get_all_experiences_for_admin(
    admin_id: str = Depends(get_current_admin)
):
    experiences = await experience_service.get_all_experiences(
        is_published=None
    )

    return {
        "total_experiences": len(experiences),
        "experiences": experiences
    }

@router.get("/{experience_id}")
async def get_experience(
    experience_id: str,
    admin_id: str = Depends(get_current_admin)
):
    experience = await experience_service.get_experience_by_id(
        experience_id
    )

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience record not found"
        )

    return experience

@router.patch("/{experience_id}")
async def update_experience(
    experience_id: str,
    experience: ExperienceUpdate,
    admin_id: str = Depends(get_current_admin)
):
    experience_data = experience.model_dump(
        exclude_unset=True
    )

    if not experience_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided"
        )

    updated = await experience_service.update_experience(
        experience_id,
        experience_data
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience record not found"
        )

    return {
        "message": "Experience record updated successfully",
        "experience_id": experience_id,
        "updated_fields": experience_data
    }

@router.delete("/{experience_id}")
async def delete_experience(
    experience_id: str,
    admin_id: str = Depends(get_current_admin)
):
    deleted = await experience_service.delete_experience(
        experience_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience record not found"
        )

    return {
        "message": "Experience record deleted successfully",
        "experience_id": experience_id
    }