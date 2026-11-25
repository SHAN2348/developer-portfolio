from pydantic import BaseModel, Field


class VisitCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class VisitResponse(BaseModel):
    id: str
    name: str
    created_at: str