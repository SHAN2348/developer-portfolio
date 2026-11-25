from datetime import datetime, timezone

from bson import ObjectId

from app.db import database


async def create_message(message_data: dict):
    collection = database.database["contact_messages"]

    message_data["id"] = str(ObjectId())
    message_data["is_read"] = False
    message_data["created_at"] = datetime.now(timezone.utc).isoformat()

    result = await collection.insert_one(message_data)

    if not result.inserted_id:
        return None

    message_data.pop("_id", None)

    return message_data


async def get_all_messages():
    collection = database.database["contact_messages"]

    cursor = collection.find().sort("created_at", -1)

    messages = await cursor.to_list(length=None)

    for message in messages:
        message.pop("_id", None)

    return messages


async def get_message_by_id(message_id: str):
    collection = database.database["contact_messages"]

    message = await collection.find_one({
        "id": message_id
    })

    if message is not None:
        message.pop("_id", None)

    return message


async def mark_message_as_read(message_id: str):
    collection = database.database["contact_messages"]

    result = await collection.update_one(
        {"id": message_id},
        {
            "$set": {
                "is_read": True
            }
        }
    )

    return result.matched_count > 0


async def delete_message(message_id: str):
    collection = database.database["contact_messages"]

    result = await collection.delete_one({
        "id": message_id
    })

    return result.deleted_count > 0