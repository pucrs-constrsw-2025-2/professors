import uuid
from fastapi import APIRouter, Depends, status, Query, Body
from typing import List, Optional

from professors.core.services.professor_service import ProfessorService
from professors.core.domain.professor_models import ProfessorCreate, ProfessorUpdate
from professors.adapters.api.schemas.professor_schemas import (
    ProfessorResponse, ProfessorCreateRequest, ProfessorUpdateRequest, ProfessorPatchRequest,
    AssociateClassRequest, ClassResponse, CourseResponse, LessonResponse
)
from professors.dependencies import get_professor_service

router = APIRouter(
    prefix="/api/v1/professors",
    tags=["Professors"]
)

# --- CRUD Principal ---

@router.post(
    "/",
    response_model=ProfessorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a Professor"
)
async def create_professor(
    professor_in: ProfessorCreateRequest,
    service: ProfessorService = Depends(get_professor_service)
):
    """Cria um novo professor.""" 
    professor_data = ProfessorCreate(**professor_in.model_dump())
    return service.create_professor(professor_data)

@router.get(
    "/",
    response_model=List[ProfessorResponse],
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
    response_model=ProfessorResponse,
    summary="Search for a specific professor"
)
async def get_professor(
    id: uuid.UUID,
    service: ProfessorService = Depends(get_professor_service)
):
    """Busca um professor específico pelo seu _id (UUID)."""
    return service.get_professor_by_id(id)

@router.put(
    "/{id}",
    response_model=ProfessorResponse,
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

@router.patch(
    "/{id}",
    response_model=ProfessorResponse,
    summary="Update an attribute from a specific professor" 
)
async def patch_professor(
    id: uuid.UUID,
    professor_in: ProfessorPatchRequest,
    service: ProfessorService = Depends(get_professor_service)
):
    """Atualiza um professor (atualização parcial - PATCH)."""
    # Envia apenas os campos que foram definidos no request
    update_data = professor_in.model_dump(exclude_unset=True)
    return service.patch_professor(id, update_data)

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

# --- Endpoints de Relacionamento (Stubs) ---

@router.get(
    "/{id}/classes",
    response_model=List[ClassResponse],
    summary="List all classes for a specific professor" 
)
async def get_professor_classes(
    id: uuid.UUID,
    service: ProfessorService = Depends(get_professor_service)
):
    """Lista todas as classes associadas a um professor.""" 
    return service.get_classes_for_professor(id)

@router.post(
    "/{id}/classes",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Associate a professor with a class" 
)
async def associate_professor_class(
    id: uuid.UUID,
    request: AssociateClassRequest,
    service: ProfessorService = Depends(get_professor_service)
):
    """Associa um professor a uma classe."""
    # service.associate_class(id, request.class_id) # (Implementação futura)
    return

@router.delete(
    "/{id}/classes/{class_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Disassociate a professor from a class"
)
async def disassociate_professor_class(
    id: uuid.UUID,
    class_id: uuid.UUID,
    service: ProfessorService = Depends(get_professor_service)
):
    """Desassocia um professor de uma classe."""
    # service.disassociate_class(id, class_id) # (Implementação futura)
    return

@router.get(
    "/{id}/courses",
    response_model=List[CourseResponse],
    summary="List all courses coordinated by a professor"
)
async def get_professor_courses(
    id: uuid.UUID,
    service: ProfessorService = Depends(get_professor_service)
):
    """Lista todos os cursos coordenados por um professor.""" 
    return service.get_courses_for_professor(id)

@router.get(
    "/{id}/lessons",
    response_model=List[LessonResponse],
    summary="List all lessons taught by a professor"
)
async def get_professor_lessons(
    id: uuid.UUID,
    service: ProfessorService = Depends(get_professor_service)
):
    """Lista todas as aulas ministradas por um professor."""
    return service.get_lessons_for_professor(id)