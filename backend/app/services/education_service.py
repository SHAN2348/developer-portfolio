from datetime import datetime, timezone

from bson import ObjectId

from app.db import database


async def create_education(education_data: dict):
    collection = database.database["portfolio_sections"]

    education_data["id"] = str(ObjectId())

    result = await collection.update_one(
        {"section_type": "education"},
        {
            "$push": {
                "content.education": education_data
            },
            "$set": {
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    if result.matched_count == 0:
        return None

    return education_data


async def get_all_education(
    is_published: bool | None = True
):
    collection = database.database["portfolio_sections"]

    query = {
        "section_type": "education"
    }

    if is_published is not None:
        query["is_published"] = is_published

    section = await collection.find_one(query)

    if section is None:
        return []

    return section.get("content", {}).get("education", [])


async def get_education_by_id(education_id: str):
    collection = database.database["portfolio_sections"]

    section = await collection.find_one({
        "section_type": "education"
    })

    if section is None:
        return None

    education_list = section.get("content", {}).get("education", [])

    for education in education_list:
        if education.get("id") == education_id:
            return education

    return None


async def update_education(
    education_id: str,
    education_data: dict
):
    collection = database.database["portfolio_sections"]

    update_fields = {
        f"content.education.$.{key}": value
        for key, value in education_data.items()
    }

    update_fields["updated_at"] = datetime.now(timezone.utc)

    result = await collection.update_one(
        {
            "section_type": "education",
            "content.education.id": education_id
        },
        {
            "$set": update_fields
        }
    )

    return result.matched_count > 0


async def delete_education(education_id: str):
    collection = database.database["portfolio_sections"]

    result = await collection.update_one(
        {
            "section_type": "education",
            "content.education.id": education_id
        },
        {
            "$pull": {
                "content.education": {
                    "id": education_id
                }
            },
            "$set": {
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return result.modified_count > 0