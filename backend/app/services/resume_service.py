from bson import ObjectId
from datetime import datetime, timezone

from app.db import database

RESUME_SECTION_TYPE = "resume"


async def create_resume(resume_data: dict):
    resume_data["id"] = str(ObjectId())

    result = await database.database["portfolio_sections"].update_one(
        {"section_type": RESUME_SECTION_TYPE},
        {
            "$push": {"content.resumes": resume_data},
            "$set": {"updated_at": datetime.now(timezone.utc)}
        }
    )

    if result.matched_count == 0:
        return None

    return resume_data


async def get_all_resumes(is_published: bool | None = True):
    query = {"section_type": RESUME_SECTION_TYPE}

    if is_published is not None:
        query["is_published"] = is_published

    section = await database.database["portfolio_sections"].find_one(query)

    if not section:
        return []

    return section.get("content", {}).get("resumes", [])


async def get_resume_by_id(resume_id: str):
    resumes = await get_all_resumes(is_published=None)

    for resume in resumes:
        if resume.get("id") == resume_id:
            return resume

    return None


async def update_resume(resume_id: str, resume_data: dict):
    result = await database.database["portfolio_sections"].update_one(
        {
            "section_type": RESUME_SECTION_TYPE,
            "content.resumes.id": resume_id
        },
        {
            "$set": {
                **{
                    f"content.resumes.$.{key}": value
                    for key, value in resume_data.items()
                },
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return result.modified_count > 0


async def replace_resume_pdf(resume_id: str, pdf_data: dict):
    result = await database.database["portfolio_sections"].update_one(
        {
            "section_type": RESUME_SECTION_TYPE,
            "content.resumes.id": resume_id
        },
        {
            "$set": {
                "content.resumes.$.pdf_url": pdf_data["secure_url"],
                "content.resumes.$.cloudinary_public_id": pdf_data["public_id"],
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return result.modified_count > 0


async def delete_resume(resume_id: str):
    result = await database.database["portfolio_sections"].update_one(
        {"section_type": RESUME_SECTION_TYPE},
        {
            "$pull": {"content.resumes": {"id": resume_id}},
            "$set": {"updated_at": datetime.now(timezone.utc)}
        }
    )

    return result.modified_count > 0