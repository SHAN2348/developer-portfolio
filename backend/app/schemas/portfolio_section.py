
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class PortfolioSectionCreate(BaseModel):
    section_type: str = Field(
        min_length=2,
        max_length=50
    )

    title: str = Field(
        min_length=2,
        max_length=100
    )

    content: dict[str, Any]

    is_published: bool = False

    display_order: int = Field(
        default=0,
        ge=0
    )


class PortfolioSectionUpdate(BaseModel):
    section_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    content: dict[str, Any] | None = None

    is_published: bool | None = None

    display_order: int | None = Field(
        default=None,
        ge=0
    )


class PortfolioSectionResponse(BaseModel):
    id: str
    section_type: str
    title: str
    content: dict[str, Any]
    is_published: bool
    display_order: int
    created_at: datetime
    updated_at: datetime
