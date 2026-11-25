from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from app.core.dependencies import get_current_admin

from app.schemas.education import (
    EducationCreate,
    EducationUpdate
)

from app.services import education_service


router = APIRouter(
    prefix="/api/education",
    tags=["Education"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create_new_education(
    education: EducationCreate,
    admin_id: str = Depends(get_current_admin)
):
    education_data = education.model_dump()

    created_education = await education_service.create_education(
        education_data
    )

    if created_education is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education section not found. Create it first."
        )

    return {
        "message": "Education record created successfully",
        "education": created_education
    }

@router.get("/")
async def get_education():
    education_list = await education_service.get_all_education()

    return {
        "total_education": len(education_list),
        "education": education_list
    }

@router.get("/admin")
async def get_all_education_for_admin(
    admin_id: str = Depends(get_current_admin)
):
    education_list = await education_service.get_all_education(
        is_published=None
    )

    return {
        "total_education": len(education_list),
        "education": education_list
    }

@router.get("/{education_id}")
async def get_education_by_id(
    education_id: str,
    admin_id: str = Depends(get_current_admin)
):
    education = await education_service.get_education_by_id(
        education_id
    )

    if education is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found"
        )

    return education

@router.patch("/{education_id}")
async def update_education(
    education_id: str,
    education: EducationUpdate,
    admin_id: str = Depends(get_current_admin)
):
    education_data = education.model_dump(
        exclude_unset=True
    )

    if not education_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided"
        )

    updated = await education_service.update_education(
        education_id,
        education_data
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found"
        )

    return {
        "message": "Education record updated successfully",
        "education_id": education_id,
        "updated_fields": education_data
    }

@router.delete("/{education_id}")
async def delete_education(
    education_id: str,
    admin_id: str = Depends(get_current_admin)
):
    deleted = await education_service.delete_education(
        education_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found"
        )

    return {
        "message": "Education record deleted successfully",
        "education_id": education_id
    }