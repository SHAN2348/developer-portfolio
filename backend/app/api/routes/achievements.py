
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_admin

from app.schemas.achievement import (
    AchievementCreate,
    AchievementUpdate
)

from app.services import achievement_service


router = APIRouter(
    prefix="/api/achievements",
    tags=["Achievements"]
)


# Public: Get published achievements
@router.get("/")
async def get_achievements():
    achievements = await achievement_service.get_all_achievements()

    return {
        "total_achievements": len(achievements),
        "achievements": achievements
    }


# Admin: Get all achievements
@router.get("/admin")
async def get_all_achievements_for_admin(
    admin_id: str = Depends(get_current_admin)
):
    achievements = await achievement_service.get_all_achievements(
        is_published=None
    )

    return {
        "total_achievements": len(achievements),
        "achievements": achievements
    }


# Admin: Create achievement
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_achievement(
    achievement_data: AchievementCreate,
    admin_id: str = Depends(get_current_admin)
):
    created_achievement = (
        await achievement_service.create_achievement(
            achievement_data.model_dump()
        )
    )

    if created_achievement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievements section not found. Create it first."
        )

    return {
        "message": "Achievement created successfully",
        "achievement": created_achievement
    }


# Admin: Update achievement
@router.patch("/{achievement_id}")
async def update_existing_achievement(
    achievement_id: str,
    achievement_data: AchievementUpdate,
    admin_id: str = Depends(get_current_admin)
):
    update_data = achievement_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one field to update."
        )

    updated = await achievement_service.update_achievement(
        achievement_id,
        update_data
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found."
        )

    achievement = await achievement_service.get_achievement_by_id(
        achievement_id
    )

    return {
        "message": "Achievement updated successfully",
        "achievement": achievement
    }


# Admin: Delete achievement
@router.delete("/{achievement_id}")
async def delete_existing_achievement(
    achievement_id: str,
    admin_id: str = Depends(get_current_admin)
):
    deleted = await achievement_service.delete_achievement(
        achievement_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found."
        )

    return {
        "message": "Achievement deleted successfully",
        "achievement_id": achievement_id
    }
