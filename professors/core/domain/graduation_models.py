import uuid
from pydantic import BaseModel, ConfigDict, Field

class GraduationBase(BaseModel):
    degree: str = Field(..., description="Nível da formação (ex: Graduação, Mestrado)")
    course: str = Field(..., description="Nome do curso")
    institution_name: str = Field(..., description="Nome da instituição de ensino")
    year: int = Field(..., description="Ano de conclusão")

class GraduationCreate(GraduationBase):
    pass

class GraduationUpdate(GraduationBase):
    pass

class Graduation(GraduationBase):
    id: uuid.UUID
    professor_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
