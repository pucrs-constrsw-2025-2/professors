import uuid
from abc import ABC, abstractmethod
from typing import List, Optional
from professors.core.domain.graduation_models import Graduation, GraduationCreate, GraduationUpdate

class GraduationRepositoryPort(ABC):
    @abstractmethod
    def add(self, professor_id: uuid.UUID, graduation_data: GraduationCreate) -> Graduation:
        pass

    @abstractmethod
    def get_by_id(self, graduation_id: uuid.UUID) -> Optional[Graduation]:
        pass

    @abstractmethod
    def get_all_for_professor(self, professor_id: uuid.UUID) -> List[Graduation]:
        pass

    @abstractmethod
    def get_all(self) -> List[Graduation]:
        pass

    @abstractmethod
    def update(self, graduation_id: uuid.UUID, graduation_data: GraduationUpdate) -> Optional[Graduation]:
        pass

    @abstractmethod
    def delete(self, graduation_id: uuid.UUID) -> bool:
        pass