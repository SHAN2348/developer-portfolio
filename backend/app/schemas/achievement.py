
from pydantic import BaseModel, Field


class AchievementCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=150
    )
    description: str = Field(
        min_length=2,
        max_length=1000
    )
    organization: str | None = None
    date: str | None = None
    display_order: int = Field(
        default=0,
        ge=0
    )


class AchievementUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )
    description: str | None = Field(
        default=None,
        min_length=2,
        max_length=1000
    )
    organization: str | None = None
    date: str | None = None
    display_order: int | None = Field(
        default=None,
        ge=0
    )


class AchievementResponse(BaseModel):
    id: str
    title: str
    description: str
    organization: str | None = None
    date: str | None = None
    display_order: int
