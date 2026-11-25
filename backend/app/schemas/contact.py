from pydantic import BaseModel, EmailStr, Field, HttpUrl


class ContactInfoUpdate(BaseModel):
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    location: str | None = Field(default=None, max_length=150)
    linkedin: HttpUrl | None = None
    github: HttpUrl | None = None