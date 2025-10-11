from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfessorBase(BaseModel):
    name: str
    email: EmailStr
    department: str

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None

class Professor(ProfessorBase):
    id: int

    class Config:
        orm_mode = True
