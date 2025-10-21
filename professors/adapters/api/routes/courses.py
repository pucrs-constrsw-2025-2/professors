import uuid
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from professors.core.services.professor_service import ProfessorService
from professors.dependencies import get_professor_service
from professors.adapters.api.schemas.course_schemas import CourseResponse
from professors.adapters.api.auth import validate_token # <-- Importado

router = APIRouter(
    prefix="/api/v1/professors/{id}/courses",
    tags=["Professors - Courses"],
    dependencies=[Depends(validate_token)] # <-- Protege todas as rotas neste arquivo
)

# Função auxiliar
async def get_professor(id: uuid.UUID, service: ProfessorService = Depends(get_professor_service)):
    return service.get_professor_by_id(id)


@router.get(
    "/",
    response_model=List[CourseResponse],
    summary="List all courses coordinated by a professor"
)
async def get_professor_courses(
    id: uuid.UUID,
    professor: dict = Depends(get_professor)
):
    """Lista todos os cursos coordenados por um professor.""" 
    return []
