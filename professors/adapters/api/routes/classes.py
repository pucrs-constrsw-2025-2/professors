import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from professors.core.services.professor_service import ProfessorService
from professors.dependencies import get_professor_service
from professors.adapters.api.schemas.class_schemas import (
    ClassResponse, AssociateClassRequest
)
from professors.adapters.api.auth import validate_token # <-- Importado

router = APIRouter(
    prefix="/api/v1/professors/{id}/classes",
    tags=["Professors - Classes"],
    dependencies=[Depends(validate_token)] # <-- Protege todas as rotas neste arquivo
)

# Função auxiliar para verificar se o professor existe
async def get_professor(id: uuid.UUID, service: ProfessorService = Depends(get_professor_service)):
    return service.get_professor_by_id(id)


@router.get(
    "/",
    response_model=List[ClassResponse],
    summary="List all classes for a specific professor" 
)
async def get_professor_classes(
    id: uuid.UUID,
    professor: dict = Depends(get_professor)
):
    """Lista todas as classes associadas a um professor.""" 
    return []

@router.post(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Associate a professor with a class" 
)
async def associate_professor_class(
    id: uuid.UUID,
    request: AssociateClassRequest,
    professor: dict = Depends(get_professor)
):
    """Associa um professor a uma classe."""
    return

@router.delete(
    "/{class_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Disassociate a professor from a class"
)
async def disassociate_professor_class(
    id: uuid.UUID,
    class_id: uuid.UUID,
    professor: dict = Depends(get_professor)
):
    """Desassocia um professor de uma classe."""
    return
