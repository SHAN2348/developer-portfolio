from fastapi import APIRouter, HTTPException, status, Query

from app.db import database
from app.schemas.project import (
                                 ProjectCreate,
                                 ProjectUpdate,
                                 ProjectResponse,
                                 ProjectListResponse,
                                 ProjectCreateResponse,
                                 ProjectUpdateResponse,
                                 ProjectDeleteResponse
                                 )
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from app.services import project_service

from fastapi import Depends
from app.core.dependencies import get_current_admin

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)

# POST
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectCreateResponse
)
async def create_project(
    project: ProjectCreate,
    admin_id: str = Depends(get_current_admin)
):
    project_data = project.model_dump(mode="json")

    project_id = await project_service.create_project(project_data)

    return {
        "message": "Project created successfully",
        "project_id": project_id,
        "project": {
            "id": project_id,
            **project_data
        }
    }
# GET all



@router.get("/", response_model=ProjectListResponse)
async def get_projects(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100)
):
    result = await project_service.get_all_projects(
        page,
        limit
    )

    total_pages = (
        result["total_projects"] + limit - 1
    ) // limit

    return {
        "total_projects": result["total_projects"],
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "projects": result["projects"]
    }



# GET by id
@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
async def get_project(project_id: str):
    project = await project_service.get_project_by_id(project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project

# UPDATE
@router.put(
    "/{project_id}",
    response_model=ProjectUpdateResponse
)
async def update_project(
    project_id: str,
    project: ProjectCreate,
    admin_id: str = Depends(get_current_admin)
):
    project_data = project.model_dump(mode="json")

    updated = await project_service.update_project(
        project_id,
        project_data
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return {
        "message": "Project updated successfully",
        "project_id": project_id,
        "updated_fields": project_data
    }

# Partial Update
@router.patch(
    "/{project_id}",
    response_model=ProjectUpdateResponse
)
async def patch_project(
    project_id: str,
    project: ProjectUpdate,
    admin_id: str = Depends(get_current_admin)
):

    project_data = project.model_dump(
        mode="json",
        exclude_unset=True
    )

    # Check whether the user provided any fields
    if not project_data:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided"
        )

    updated = await project_service.patch_project(
        project_id,
        project_data
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return {
        "message": "Project partially updated successfully",
        "project_id": project_id,
        "updated_fields": project_data
    }

# DELETE
@router.delete(
    "/{project_id}",
    response_model=ProjectDeleteResponse
)
async def delete_project(
    project_id: str,
    admin_id: str = Depends(get_current_admin)
):
    deleted = await project_service.delete_project(project_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return {
        "message": "Project deleted successfully",
        "project_id": project_id
    }