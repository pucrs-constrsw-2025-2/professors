import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

# Modelo base com os campos comuns
class ProfessorBase(BaseModel):
    name: str = Field(..., description="Nome Completo do Professor")
    registration_number: int = Field(..., description="Número de matrícula (Inteiro)")
    institucional_email: EmailStr = Field(..., description="E-mail institucional")
    status: str = Field(..., description="Status (ex: active, inactive, on_leave)")

# Modelo para criação (usado pelo serviço)
class ProfessorCreate(ProfessorBase):
    pass

# Modelo para atualização (usado pelo serviço)
class ProfessorUpdate(ProfessorBase):
    pass

class Professor(ProfessorBase):
    id: uuid.UUID = Field(..., description="ID único do registro no banco (UUID)")

    model_config = ConfigDict(
        from_attributes=True
    )