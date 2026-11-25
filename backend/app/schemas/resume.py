from pydantic import BaseModel, Field, HttpUrl


class ResumeCreate(BaseModel):
    title: str = Field(default="My Resume", min_length=2, max_length=100)
    display_order: int = Field(default=10, ge=0)


class ResumeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    display_order: int | None = Field(default=None, ge=0)


class ResumeResponse(BaseModel):
    id: str
    title: str
    pdf_url: HttpUrl
    display_order: int