import uuid
from pydantic import BaseModel, Field

class GraduationBase(BaseModel):
    degree: str = Field(..., description="Nível da formação (ex: Graduação, Mestrado)")
    course: str = Field(..., description="Nome do curso")
    institution_name: str = Field(..., description="Nome da instituição de ensino")
    year: int = Field(..., description="Ano de conclusão")

class GraduationCreateRequest(GraduationBase):
    pass

class GraduationUpdateRequest(GraduationBase):
    pass

class GraduationResponse(GraduationBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
