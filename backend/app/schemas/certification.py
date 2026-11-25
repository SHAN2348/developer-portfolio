
from pydantic import BaseModel, Field, HttpUrl


class CertificationCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    issuing_organization: str = Field(
        min_length=2,
        max_length=150
    )
    issue_date: str | None = None
    display_order: int = Field(default=0, ge=0)


class CertificationUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )
    issuing_organization: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )
    issue_date: str | None = None
    display_order: int | None = Field(default=None, ge=0)


class CertificationResponse(BaseModel):
    id: str
    title: str
    issuing_organization: str
    issue_date: str | None = None
    pdf_url: HttpUrl
    display_order: int
