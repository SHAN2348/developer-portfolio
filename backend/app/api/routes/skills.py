from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from app.core.dependencies import get_current_admin

from app.schemas.skill import (
    SkillCreate,
    SkillUpdate,
    SkillResponse
)

from app.services import skill_service

router = APIRouter(
    prefix="/api/skills",
    tags=["Skills"]
)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create_new_skill(
    skill: SkillCreate,
    admin_id: str = Depends(get_current_admin)
):
    skill_data = skill.model_dump()

    created_skill = await skill_service.create_skill(
        skill_data
    )

    if created_skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skills section not found. Create it first."
        )

    return {
        "message": "Skill created successfully",
        "skill": created_skill
    }

@router.get("/")
async def get_skills():
    skills = await skill_service.get_all_skills()

    return {
        "total_skills": len(skills),
        "skills": skills
    }

@router.get("/admin")
async def get_all_skills_for_admin(
    admin_id: str = Depends(get_current_admin)
):
    skills = await skill_service.get_all_skills(
        is_published=None
    )

    return {
        "total_skills": len(skills),
        "skills": skills
    }

@router.get("/{skill_id}")
async def get_skill(
    skill_id: str,
    admin_id: str = Depends(get_current_admin)
):
    skill = await skill_service.get_skill_by_id(skill_id)

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )

    return skill

@router.patch("/{skill_id}")
async def update_skill(
    skill_id: str,
    skill: SkillUpdate,
    admin_id: str = Depends(get_current_admin)
):
    skill_data = skill.model_dump(exclude_unset=True)

    if not skill_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided"
        )

    updated = await skill_service.update_skill(
        skill_id,
        skill_data
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )

    return {
        "message": "Skill updated successfully",
        "skill_id": skill_id,
        "updated_fields": skill_data
    }

@router.delete("/{skill_id}")
async def delete_skill(
    skill_id: str,
    admin_id: str = Depends(get_current_admin)
):
    deleted = await skill_service.delete_skill(skill_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )

    return {
        "message": "Skill deleted successfully",
        "skill_id": skill_id
    }