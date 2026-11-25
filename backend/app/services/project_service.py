from app.db import database
from bson import ObjectId
from bson.errors import InvalidId


async def create_project(project_data: dict):

    result = await database.database["projects"].insert_one(
        project_data
    )

    return str(result.inserted_id)



async def get_all_projects(page: int = 1, limit: int = 10):
    projects = []

    skip = (page - 1) * limit

    collection = database.database["projects"]

    # Get total number of projects
    total_projects = await collection.count_documents({})

    # Get projects for the requested page
    cursor = (
        collection.find()
        .sort("_id", 1)
        .skip(skip)
        .limit(limit)
    )

    async for project in cursor:
        project["id"] = str(project.pop("_id"))
        projects.append(project)

    return {
        "total_projects": total_projects,
        "page": page,
        "limit": limit,
        "projects": projects
    }



async def get_project_by_id(project_id: str):
    try:
        object_id = ObjectId(project_id)
    except InvalidId:
        return None

    project = await database.database["projects"].find_one(
        {"_id": object_id}
    )

    if project is None:
        return None

    project["id"] = str(project.pop("_id"))

    return project

#
async def delete_project(project_id: str):
    try:
        object_id = ObjectId(project_id)
    except InvalidId:
        return False

    result = await database.database["projects"].delete_one(
        {"_id": object_id}
    )

    return result.deleted_count > 0

async def update_project(project_id: str, project_data: dict):
    try:
        object_id = ObjectId(project_id)
    except InvalidId:
        return False

    result = await database.database["projects"].update_one(
        {"_id": object_id},
        {"$set": project_data}
    )

    return result.matched_count > 0

async def patch_project(project_id: str, project_data: dict):
    try:
        object_id = ObjectId(project_id)
    except InvalidId:
        return False

    if not project_data:
        return False

    result = await database.database["projects"].update_one(
        {"_id": object_id},
        {"$set": project_data}
    )

    return result.matched_count > 0