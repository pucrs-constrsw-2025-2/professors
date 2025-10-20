from sqlalchemy.orm import Session
from fastapi import Depends

from professors.adapters.database.database import get_db
from professors.adapters.database.professor_repository import SQLAlchemyProfessorRepository
from professors.core.ports.professor_repository_port import ProfessorRepositoryPort
from professors.core.services.professor_service import ProfessorService

def get_professor_repository(db: Session = Depends(get_db)) -> ProfessorRepositoryPort:
    """Retorna uma instância concreta do repositório."""
    return SQLAlchemyProfessorRepository(db)

def get_professor_service(
    repo: ProfessorRepositoryPort = Depends(get_professor_repository)
) -> ProfessorService:
    """Retorna uma instância do serviço, injetando o repositório."""
    return ProfessorService(repo)