import uuid
from typing import List
from fastapi import HTTPException, status
from professors.core.ports.graduation_repository_port import GraduationRepositoryPort
from professors.core.domain.graduation_models import Graduation, GraduationCreate, GraduationUpdate

class GraduationService:
    def __init__(self, repository: GraduationRepositoryPort):
        self.repository = repository

    def create_graduation(self, professor_id: uuid.UUID, graduation_data: GraduationCreate) -> Graduation:
        return self.repository.add(professor_id, graduation_data)

    def get_graduation_by_id(self, graduation_id: uuid.UUID) -> Graduation:
        graduation = self.repository.get_by_id(graduation_id)
        if not graduation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Graduation not found.")
        return graduation

    def get_all_graduations_for_professor(self, professor_id: uuid.UUID) -> List[Graduation]:
        return self.repository.get_all_for_professor(professor_id)

    def get_all_graduations(self) -> List[Graduation]:
        return self.repository.get_all()

    def update_graduation(self, graduation_id: uuid.UUID, graduation_data: GraduationUpdate) -> Graduation:
        updated = self.repository.update(graduation_id, graduation_data)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Graduation not found.")
        return updated

    def delete_graduation(self, graduation_id: uuid.UUID) -> None:
        if not self.repository.delete(graduation_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Graduation not found.")