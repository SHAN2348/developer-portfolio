from datetime import datetime, timezone

from bson import ObjectId

from app.db import database


async def create_experience(experience_data: dict):
    collection = database.database["portfolio_sections"]

    experience_data["id"] = str(ObjectId())

    result = await collection.update_one(
        {"section_type": "experience"},
        {
            "$push": {
                "content.experience": experience_data
            },
            "$set": {
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    if result.matched_count == 0:
        return None

    return experience_data


async def get_all_experiences(
    is_published: bool | None = True
):
    collection = database.database["portfolio_sections"]

    query = {
        "section_type": "experience"
    }

    if is_published is not None:
        query["is_published"] = is_published

    section = await collection.find_one(query)

    if section is None:
        return []

    return section.get("content", {}).get("experience", [])


async def get_experience_by_id(experience_id: str):
    collection = database.database["portfolio_sections"]

    section = await collection.find_one({
        "section_type": "experience"
    })

    if section is None:
        return None

    experiences = section.get("content", {}).get("experience", [])

    for experience in experiences:
        if experience.get("id") == experience_id:
            return experience

    return None


async def update_experience(
    experience_id: str,
    experience_data: dict
):
    collection = database.database["portfolio_sections"]

    update_fields = {
        f"content.experience.$.{key}": value
        for key, value in experience_data.items()
    }

    update_fields["updated_at"] = datetime.now(timezone.utc)

    result = await collection.update_one(
        {
            "section_type": "experience",
            "content.experience.id": experience_id
        },
        {
            "$set": update_fields
        }
    )

    return result.matched_count > 0


async def delete_experience(experience_id: str):
    collection = database.database["portfolio_sections"]

    result = await collection.update_one(
        {
            "section_type": "experience",
            "content.experience.id": experience_id
        },
        {
            "$pull": {
                "content.experience": {
                    "id": experience_id
                }
            },
            "$set": {
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return result.modified_count > 0