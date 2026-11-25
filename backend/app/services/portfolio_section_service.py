
from datetime import datetime, timezone

from app.db import database



async def create_section(section_data: dict):
    collection = database.database["portfolio_sections"]

    now = datetime.now(timezone.utc)

    section_data["created_at"] = now
    section_data["updated_at"] = now

    result = await collection.insert_one(section_data)

    return str(result.inserted_id)



async def get_all_sections(is_published: bool | None = None):
    collection = database.database["portfolio_sections"]

    query = {}

    if is_published is not None:
        query["is_published"] = is_published

    cursor = collection.find(query).sort(
        "display_order", 1
    )

    sections = []

    async for section in cursor:
        section["id"] = str(section.pop("_id"))
        sections.append(section)

    return sections


from bson import ObjectId
from bson.errors import InvalidId


async def get_section_by_id(section_id: str):
    try:
        object_id = ObjectId(section_id)
    except InvalidId:
        return None

    collection = database.database["portfolio_sections"]

    section = await collection.find_one({
        "_id": object_id
    })

    if section is None:
        return None

    section["id"] = str(section.pop("_id"))

    return section

async def update_section(
    section_id: str,
    section_data: dict
):
    try:
        object_id = ObjectId(section_id)
    except InvalidId:
        return False

    collection = database.database["portfolio_sections"]

    section_data["updated_at"] = datetime.now(timezone.utc)

    result = await collection.update_one(
        {"_id": object_id},
        {"$set": section_data}
    )

    return result.matched_count > 0

async def delete_section(section_id: str):
    try:
        object_id = ObjectId(section_id)
    except InvalidId:
        return False

    collection = database.database["portfolio_sections"]

    result = await collection.delete_one({
        "_id": object_id
    })

    return result.deleted_count > 0