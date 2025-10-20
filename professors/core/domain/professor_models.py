import uuid
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Modelo base com os campos comuns
class ProfessorBase(BaseModel):
    id_professor: str = Field(..., description="ID lógico do professor (ex: 12345)")
    name: str = Field(..., description="Nome Completo do Professor")
    registration_number: str = Field(..., description="Número de matrícula SIAPE")
    institucional_email: EmailStr = Field(..., description="E-mail institucional")
    status: str = Field(..., description="Status (ex: active, inactive, on_leave)")

# Modelo para criação (usado pelo serviço)
class ProfessorCreate(ProfessorBase):
    pass

# Modelo para atualização (usado pelo serviço)
class ProfessorUpdate(ProfessorBase):
    pass

# Modelo completo do domínio (inclui o _id do banco)
class Professor(ProfessorBase):
    db_id: uuid.UUID = Field(..., alias="_id", description="ID único do registro no banco (UUID)")

    class Config:
        from_attributes = True # Antigo orm_mode