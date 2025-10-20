import uuid
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from professors.core.domain.professor_models import Professor, ProfessorCreate, ProfessorUpdate

class ProfessorRepositoryPort(ABC):
    """Porta de interface para o repositório de professores."""

    @abstractmethod
    def add(self, professor_data: ProfessorCreate) -> Professor:
        """Cria um novo professor no banco."""
        pass

    @abstractmethod
    def get_by_id(self, professor_uuid: uuid.UUID) -> Optional[Professor]:
        """Busca um professor pelo seu _id (UUID)."""
        pass

    @abstractmethod
    def get_by_id_professor(self, id_professor: str) -> Optional[Professor]:
        """Busca um professor pelo seu id_professor (lógico)."""
        pass

    @abstractmethod
    def get_by_registration_number(self, reg_number: str) -> Optional[Professor]:
        """Busca um professor pelo seu registration_number."""
        pass

    @abstractmethod
    def get_all(self) -> List[Professor]:
        """Retorna todos os professores."""
        pass
    
    @abstractmethod
    def search(self, params: Dict[str, Any]) -> List[Professor]:
        """Busca professores com base em critérios (filtros)."""
        pass

    @abstractmethod
    def update(self, professor_uuid: uuid.UUID, professor_data: Dict[str, Any]) -> Optional[Professor]:
        """Atualiza um professor (parcial ou completo)."""
        pass

    @abstractmethod
    def delete(self, professor_uuid: uuid.UUID) -> bool:
        """Deleta um professor pelo seu _id (UUID)."""
        pass