import uuid
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from professors.core.services.professor_service import ProfessorService
from professors.dependencies import get_professor_service
from professors.adapters.api.schemas.lesson_schemas import LessonResponse
from professors.adapters.api.auth import validate_token # <-- Importado

router = APIRouter(
    prefix="/api/v1/professors/{id}/lessons",
    tags=["Professors - Lessons"],
    dependencies=[Depends(validate_token)] # <-- Protege todas as rotas neste arquivo
)

# Função auxiliar
async def get_professor(id: uuid.UUID, service: ProfessorService = Depends(get_professor_service)):
    return service.get_professor_by_id(id)


@router.get(
    "/",
    response_model=List[LessonResponse],
    summary="List all lessons taught by a professor"
)
async def get_professor_lessons(
    id: uuid.UUID,
    professor: dict = Depends(get_professor)
):
    """Lista todas as aulas ministradas por um professor."""
    return []
