import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import List, Optional

from professors.core.domain.professor_models import Professor, ProfessorCreate, ProfessorUpdate
from professors.core.services.professor_service import ProfessorService
from professors.adapters.api.schemas.professor_schemas import (
    ProfessorResponse, ProfessorCreateRequest, ProfessorUpdateRequest
)
from professors.dependencies import get_professor_service
from professors.adapters.api.auth import validate_token  # <-- Importado

router = APIRouter(
    prefix="/api/v1/professors",
    tags=["Professors"],
    dependencies=[Depends(validate_token)]
)

# --- CRUD Principal ---

@router.post(
    "/",
    response_model=Professor,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new professor"
)
def create_professor(
    professor_data: ProfessorCreateRequest,
    service: ProfessorService = Depends(get_professor_service)
):
    try:
        professor_create = ProfessorCreate(**professor_data.model_dump())
        created_professor = service.create_professor(professor_create)
        return created_professor
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar professor: {str(e)}"
        )

@router.get(
    "/",
    response_model=List[Professor],
    summary="Search for professors" 
)
async def search_professors(
    name: Optional[str] = Query(None, description="Filtrar por nome (parcial)"),
    status: Optional[str] = Query(None, description="Filtrar por status (exato)"),
    service: ProfessorService = Depends(get_professor_service)
):
    """Busca todos os professores ou filtra por critérios.""" 
    if name or status:
        params = {"name": name, "status": status}
        return service.search_professors(params)
    return service.get_all_professors()

@router.get(
    "/{id}",
    response_model=Professor,
    summary="Search for a specific professor"
)
async def get_professor(
    id: uuid.UUID,
    service: ProfessorService = Depends(get_professor_service)
):
    """Busca um professor específico pelo seu id (UUID)."""
    return service.get_professor_by_id(id)

@router.put(
    "/{id}",
    response_model=Professor,
    summary="Update a specific professor"
)
async def update_professor(
    id: uuid.UUID,
    professor_in: ProfessorUpdateRequest,
    service: ProfessorService = Depends(get_professor_service)
):
    """Atualiza um professor (substituição completa - PUT).""" 
    professor_data = ProfessorUpdate(**professor_in.model_dump())
    return service.update_professor(id, professor_data)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific professor" 
)
async def delete_professor(
    id: uuid.UUID,
    service: ProfessorService = Depends(get_professor_service)
):
    """Deleta um professor específico."""
    service.delete_professor(id)
    return
