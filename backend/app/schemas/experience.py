from pydantic import BaseModel, Field


class ExperienceCreate(BaseModel):
    company: str = Field(min_length=2, max_length=150)
    job_title: str = Field(min_length=2, max_length=100)
    employment_type: str = Field(default="Full-time")
    location: str | None = None
    start_date: str
    end_date: str | None = None
    currently_working: bool = False
    description: str = ""
    display_order: int = Field(default=0, ge=0)


class ExperienceUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=2, max_length=150)
    job_title: str | None = Field(default=None, min_length=2, max_length=100)
    employment_type: str | None = None
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    currently_working: bool | None = None
    description: str | None = None
    display_order: int | None = Field(default=None, ge=0)


class ExperienceResponse(BaseModel):
    id: str
    company: str
    job_title: str
    employment_type: str
    location: str | None = None
    start_date: str
    end_date: str | None = None
    currently_working: bool
    description: str
    display_order: int