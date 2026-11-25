from datetime import datetime, timezone

from bson import ObjectId

from app.db import database


async def create_skill(skill_data: dict):
    collection = database.database["portfolio_sections"]

    skill_data["id"] = str(ObjectId())

    result = await collection.update_one(
        {"section_type": "skills"},
        {
            "$push": {
                "content.skills": skill_data
            },
            "$set": {
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    if result.matched_count == 0:
        return None

    return skill_data

async def get_all_skills(
    is_published: bool | None = True
):
    collection = database.database["portfolio_sections"]

    query = {
        "section_type": "skills"
    }

    if is_published is not None:
        query["is_published"] = is_published

    section = await collection.find_one(query)

    if section is None:
        return []

    return section.get("content", {}).get("skills", [])

async def get_skill_by_id(skill_id: str):
    collection = database.database["portfolio_sections"]

    section = await collection.find_one({
        "section_type": "skills"
    })

    if section is None:
        return None

    skills = section.get("content", {}).get("skills", [])

    for skill in skills:
        if skill.get("id") == skill_id:
            return skill

    return None

async def update_skill(skill_id: str, skill_data: dict):
    collection = database.database["portfolio_sections"]

    update_fields = {
        f"content.skills.$.{key}": value
        for key, value in skill_data.items()
    }

    update_fields["updated_at"] = datetime.now(timezone.utc)

    result = await collection.update_one(
        {
            "section_type": "skills",
            "content.skills.id": skill_id
        },
        {
            "$set": update_fields
        }
    )

    return result.matched_count > 0

async def delete_skill(skill_id: str):
    collection = database.database["portfolio_sections"]

    result = await collection.update_one(
        {
            "section_type": "skills",
            "content.skills.id": skill_id
        },
        {
            "$pull": {
                "content.skills": {
                    "id": skill_id
                }
            },
            "$set": {
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return result.modified_count > 0