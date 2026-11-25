from datetime import datetime, timezone

from bson import ObjectId

from app.db import database


async def create_visit(visit_data: dict):
    collection = database.database["visits"]

    visit_data["id"] = str(ObjectId())
    visit_data["created_at"] = datetime.now(timezone.utc).isoformat()

    result = await collection.insert_one(visit_data)

    if not result.inserted_id:
        return None

    visit_data.pop("_id", None)

    return visit_data


async def get_all_visits():
    collection = database.database["visits"]

    cursor = collection.find().sort("created_at", -1)

    visits = await cursor.to_list(length=None)

    for visit in visits:
        visit.pop("_id", None)

    return visits


async def get_visit_summary():
    visits = await get_all_visits()

    unique_names = {visit["name"].strip().lower() for visit in visits}

    return {
        "total_visits": len(visits),
        "unique_visitors": len(unique_names),
    }