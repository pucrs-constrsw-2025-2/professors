import uuid
from typing import List, Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from professors.core.ports.professor_repository_port import ProfessorRepositoryPort
from professors.core.domain.professor_models import Professor, ProfessorCreate, ProfessorUpdate

class ProfessorService:
    """Serviço com a lógica de negócios para professores."""
    
    def __init__(self, repository: ProfessorRepositoryPort):
        self.repository = repository

    def create_professor(self, professor_data: ProfessorCreate) -> Professor:
        if self.repository.get_by_registration_number(professor_data.registration_number):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Professor with registration_number '{professor_data.registration_number}' already exists."
            )
            
        return self.repository.add(professor_data)

    def get_professor_by_id(self, professor_uuid: uuid.UUID) -> Professor:
        professor = self.repository.get_by_id(professor_uuid)
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor not found."
            ) 
        return professor

    def get_all_professors(self) -> List[Professor]:
        return self.repository.get_all()

    def search_professors(self, params: Dict[str, Any]) -> List[Professor]:
        search_params = {k: v for k, v in params.items() if v is not None}
        return self.repository.search(search_params)

    def update_professor(self, professor_uuid: uuid.UUID, professor_data: ProfessorUpdate) -> Professor:
        updated_professor = self.repository.update(
            professor_uuid, 
            professor_data.model_dump()
        )
        if not updated_professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor not found."
            ) 
        return updated_professor

    def delete_professor(self, professor_uuid: uuid.UUID) -> None:
        success = self.repository.delete(professor_uuid)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor not found."
            ) 
        return
