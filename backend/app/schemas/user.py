from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str = 'ADMIN'

    model_config = {'from_attributes': True}
