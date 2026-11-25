from pydantic import BaseModel, EmailStr, Field


class ContactMessageCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    subject: str = Field(min_length=3, max_length=150)
    message: str = Field(min_length=10, max_length=5000)


class ContactMessageResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    subject: str
    message: str
    is_read: bool = False
    created_at: str