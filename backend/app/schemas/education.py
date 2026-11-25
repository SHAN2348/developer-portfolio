from pydantic import BaseModel, Field


class EducationCreate(BaseModel):
    institution: str = Field(
        min_length=2,
        max_length=150
    )

    degree: str = Field(
        min_length=2,
        max_length=100
    )

    field_of_study: str = Field(
        min_length=2,
        max_length=100
    )

    start_year: int = Field(
        ge=1950,
        le=2100
    )

    end_year: int | None = Field(
        default=None,
        ge=1950,
        le=2100
    )

    grade: str | None = None

    description: str | None = None

    display_order: int = Field(
        default=0,
        ge=0
    )


class EducationUpdate(BaseModel):
    institution: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    degree: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    field_of_study: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    start_year: int | None = Field(
        default=None,
        ge=1950,
        le=2100
    )

    end_year: int | None = Field(
        default=None,
        ge=1950,
        le=2100
    )

    grade: str | None = None

    description: str | None = None

    display_order: int | None = Field(
        default=None,
        ge=0
    )


class EducationResponse(BaseModel):
    id: str
    institution: str
    degree: str
    field_of_study: str
    start_year: int
    end_year: int | None = None
    grade: str | None = None
    description: str | None = None
    display_order: int