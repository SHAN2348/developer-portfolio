
from app.db import database
from app.core.password import hash_password


async def get_admin_by_username(username: str):
    collection = database.database["admins"]

    admin = await collection.find_one({
        "username": username
    })

    return admin


async def create_admin(username: str, password: str):
    collection = database.database["admins"]

    existing_admin = await get_admin_by_username(username)

    if existing_admin:
        return None

    admin_data = {
        "username": username,
        "password_hash": hash_password(password)
    }

    result = await collection.insert_one(admin_data)

    return str(result.inserted_id)
