from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_admin
from app.schemas.visit import VisitCreate
from app.services import visit_service


router = APIRouter(
    prefix="/api/visits",
    tags=["Visits"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def record_visit(visit_data: VisitCreate):
    created_visit = await visit_service.create_visit(
        visit_data.model_dump()
    )

    if created_visit is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to record visit."
        )

    return {
        "message": "Visit recorded.",
        "visit": created_visit
    }


@router.get("/admin")
async def get_visits_for_admin(
    admin_id: str = Depends(get_current_admin)
):
    summary = await visit_service.get_visit_summary()
    visits = await visit_service.get_all_visits()

    return {
        "total_visits": summary["total_visits"],
        "unique_visitors": summary["unique_visitors"],
        "visits": visits
    }