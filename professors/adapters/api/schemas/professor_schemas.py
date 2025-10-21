import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional, List, Any

# Campos base do professor
class ProfessorBase(BaseModel):
    name: str = Field(..., description="Nome Completo do Professor")
    registration_number: int = Field(..., description="Número de matrícula (Inteiro)")
    institucional_email: EmailStr = Field(..., description="E-mail institucional")
    status: str = Field(..., description="Status (ex: active, inactive, on_leave)")

# Schema para o Request Body do POST
class ProfessorCreateRequest(ProfessorBase):
    pass

# Schema para o Response Body (GET, POST, PUT)
class ProfessorResponse(ProfessorBase):
    id: uuid.UUID = Field(..., description="ID único do registro no banco (UUID)")
    
    model_config = ConfigDict(
        from_attributes=True,
    )

# Schema para o Request Body do PUT
class ProfessorUpdateRequest(ProfessorBase):
    pass