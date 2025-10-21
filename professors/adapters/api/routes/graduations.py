import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from professors.dependencies import get_professor_service, get_graduation_service
from professors.core.services.professor_service import ProfessorService
from professors.core.services.graduation_service import GraduationService
from professors.core.domain.graduation_models import GraduationCreate, GraduationUpdate
from professors.adapters.api.schemas.graduation_schemas import (
    GraduationCreateRequest,
    GraduationResponse,
    GraduationUpdateRequest,
)
from professors.adapters.api.auth import validate_token

# UM Roteador, sem prefixo geral.
# A tag "Graduations" será usada para todos.
router = APIRouter(
    tags=["Graduations"],
    dependencies=[Depends(validate_token)]
)

# Dependência para garantir que o professor existe (usada nas rotas aninhadas)
async def get_professor(professor_id: uuid.UUID, service: ProfessorService = Depends(get_professor_service)):
    return service.get_professor_by_id(professor_id)


# POST - /api/v1/professors/{professor_id}/graduations/
@router.post(
    "/api/v1/professors/{professor_id}/graduations/",
    response_model=GraduationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar graduação para um professor"
)
def create_graduation(
    professor_id: uuid.UUID,
    request: GraduationCreateRequest,
    service: GraduationService = Depends(get_graduation_service),
    professor: dict = Depends(get_professor) # Valida o professor
):
    graduation_create = GraduationCreate(**request.model_dump())
    return service.create_graduation(professor_id, graduation_create)

# GET (id prof) - /api/v1/professors/{professor_id}/graduations/
@router.get(
    "/api/v1/professors/{professor_id}/graduations/",
    response_model=List[GraduationResponse],
    summary="Listar graduações de um professor específico"
)
def get_all_graduations_for_professor(
    professor_id: uuid.UUID,
    service: GraduationService = Depends(get_graduation_service),
    professor: dict = Depends(get_professor) # Valida o professor
):
    return service.get_all_graduations_for_professor(professor_id)

# PUT - /api/v1/professors/{professor_id}/graduations/{graduation_id}
@router.put(
    "/api/v1/professors/{professor_id}/graduations/{graduation_id}",
    response_model=GraduationResponse,
    summary="Atualizar uma graduação"
)
def update_graduation(
    graduation_id: uuid.UUID,
    request: GraduationUpdateRequest,
    professor_id: uuid.UUID, # Pega do path
    service: GraduationService = Depends(get_graduation_service),
    professor: dict = Depends(get_professor) # Valida o professor
):
    # O professor_id aqui serve para validar o path e a existência do professor.
    graduation_update = GraduationUpdate(**request.model_dump())
    return service.update_graduation(graduation_id, graduation_update)

# DELETE - /api/v1/professors/{professor_id}/graduations/{graduation_id}
@router.delete(
    "/api/v1/professors/{professor_id}/graduations/{graduation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir uma graduação"
)
def delete_graduation(
    graduation_id: uuid.UUID,
    professor_id: uuid.UUID, # Pega do path
    service: GraduationService = Depends(get_graduation_service),
    professor: dict = Depends(get_professor) # Valida o professor
):
    # Valida o professor antes de tentar deletar
    service.delete_graduation(graduation_id)


# --- Endpoint Geral (Independente do Professor) ---

# GET ALL - /api/v1/graduations/
@router.get(
    "/api/v1/graduations/",
    response_model=List[GraduationResponse],
    summary="Listar todas as graduações do sistema"
)
def get_all_graduations(
    service: GraduationService = Depends(get_graduation_service)
):
    """
    Lista todas as graduações cadastradas no sistema,
    independentemente do professor.
    """
    return service.get_all_graduations()