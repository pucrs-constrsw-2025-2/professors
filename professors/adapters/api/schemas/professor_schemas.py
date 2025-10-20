import uuid
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any

# --- Schemas para o CRUD de Professores ---

# Campos base do professor [cite: 2]
class ProfessorBase(BaseModel):
    id_professor: str = Field(..., description="ID lógico do professor (ex: 12345)")
    name: str = Field(..., description="Nome Completo do Professor")
    registration_number: str = Field(..., description="Número de matrícula SIAPE")
    institucional_email: EmailStr = Field(..., description="E-mail institucional")
    status: str = Field(..., description="Status (ex: active, inactive, on_leave)")

# Schema para o Request Body do POST [cite: 2]
class ProfessorCreateRequest(ProfessorBase):
    pass

# Schema para o Response Body (GET, POST, PUT, PATCH) [cite: 5]
class ProfessorResponse(ProfessorBase):
    db_id: uuid.UUID = Field(..., alias="_id", description="ID único do registro no banco (UUID)")

# Schema para o Request Body do PUT [cite: 12]
# (message.txt indica um body completo)
class ProfessorUpdateRequest(ProfessorBase):
    pass

# Schema para o Request Body do PATCH [cite: 15]
# (message.txt indica um body parcial)
class ProfessorPatchRequest(BaseModel):
    id_professor: Optional[str] = None
    name: Optional[str] = None
    registration_number: Optional[str] = None
    institucional_email: Optional[EmailStr] = None
    status: Optional[str] = None


# --- Schemas para Endpoints de Relacionamento ---
# (Definidos conforme message.txt, mas podem ser ajustados)

# Exemplo de resposta para GET /{{id}}/classes [cite: 19]
class ClassResponse(BaseModel):
    id: uuid.UUID
    name: str
    semester: str
    # ... outros dados da classe

# Request body para POST /{{id}}/classes [cite: 20]
class AssociateClassRequest(BaseModel):
    class_id: uuid.UUID
    
# Exemplo de resposta para GET /{{id}}/courses [cite: 23]
class CourseResponse(BaseModel):
    id: uuid.UUID
    name: str
    # ... outros dados do curso

# Exemplo de resposta para GET /{{id}}/lessons [cite: 25]
class LessonResponse(BaseModel):
    id: uuid.UUID
    topic: str
    date: str # Ou datetime
    # ... outros dados da aula