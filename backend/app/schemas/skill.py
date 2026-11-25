from pydantic import BaseModel, Field


class SkillCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=50
    )

    category: str = Field(
        min_length=2,
        max_length=50
    )

    proficiency: str = Field(
        default="Beginner"
    )

    display_order: int = Field(
        default=0,
        ge=0
    )

class SkillUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    category: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    proficiency: str | None = None

    display_order: int | None = Field(
        default=None,
        ge=0
    )

class SkillResponse(BaseModel):
    id: str

    name: str

    category: str

    proficiency: str

    display_order: int