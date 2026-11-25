
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import AsyncMongoClient

# Load environment variables from backend/.env
BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")

# MongoDB configuration
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "developer_portfolio")

# Global database objects
client = None
database = None


async def connect_to_mongodb():
    global client, database

    if not MONGODB_URI:
        raise ValueError("MONGODB_URI is missing from .env")

    try:
        client = AsyncMongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=5000
        )

        # Verify connection
        await client.admin.command("ping")

        database = client[DATABASE_NAME]

        print("MongoDB Atlas connected successfully!")

    except Exception:
        if client is not None:
            client.close()
            client = None

        raise


async def close_mongodb_connection():
    global client, database

    if client is not None:
        await client.close()
        client = None
        database = None

        print("MongoDB connection closed.")
