
from datetime import datetime, timezone

from bson import ObjectId

from app.db import database


async def create_achievement(achievement_data: dict):
    collection = database.database["portfolio_sections"]

    achievement_data["id"] = str(ObjectId())

    result = await collection.update_one(
        {"section_type": "achievements"},
        {
            "$push": {
                "content.achievements": achievement_data
            },
            "$set": {
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    if result.matched_count == 0:
        return None

    return achievement_data


async def get_all_achievements(
    is_published: bool | None = True
):
    collection = database.database["portfolio_sections"]

    query = {
        "section_type": "achievements"
    }

    if is_published is not None:
        query["is_published"] = is_published

    section = await collection.find_one(query)

    if section is None:
        return []

    return section.get("content", {}).get("achievements", [])


async def get_achievement_by_id(achievement_id: str):
    collection = database.database["portfolio_sections"]

    section = await collection.find_one({
        "section_type": "achievements"
    })

    if section is None:
        return None

    achievements = section.get("content", {}).get("achievements", [])

    for achievement in achievements:
        if achievement.get("id") == achievement_id:
            return achievement

    return None


async def update_achievement(
    achievement_id: str,
    achievement_data: dict
):
    collection = database.database["portfolio_sections"]

    update_fields = {
        f"content.achievements.$.{key}": value
        for key, value in achievement_data.items()
    }

    update_fields["updated_at"] = datetime.now(timezone.utc)

    result = await collection.update_one(
        {
            "section_type": "achievements",
            "content.achievements.id": achievement_id
        },
        {
            "$set": update_fields
        }
    )

    return result.matched_count > 0


async def delete_achievement(achievement_id: str):
    collection = database.database["portfolio_sections"]

    result = await collection.update_one(
        {
            "section_type": "achievements",
            "content.achievements.id": achievement_id
        },
        {
            "$pull": {
                "content.achievements": {
                    "id": achievement_id
                }
            },
            "$set": {
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return result.modified_count > 0
