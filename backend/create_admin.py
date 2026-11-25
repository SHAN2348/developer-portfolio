
import asyncio
from getpass import getpass

from app.db.database import (
    connect_to_mongodb,
    close_mongodb_connection
)
from app.schemas.admin import AdminCreate
from app.services.admin_service import create_admin


async def main():
    username = input("Enter admin username: ").strip()
    password = getpass("Enter admin password: ")
    confirm_password = getpass("Confirm admin password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    try:
        admin = AdminCreate(
            username=username,
            password=password
        )
    except Exception as error:
        print(f"Invalid admin details: {error}")
        return

    await connect_to_mongodb()

    try:
        admin_id = await create_admin(
            admin.username,
            admin.password
        )

        if admin_id is None:
            print("This admin username already exists.")
        else:
            print("Admin account created successfully!")
            print(f"Admin ID: {admin_id}")

    finally:
        await close_mongodb_connection()


if __name__ == "__main__":
    asyncio.run(main())
