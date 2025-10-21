from sqlalchemy.orm import Session
from fastapi import Depends

from professors.adapters.database.database import get_db
from professors.adapters.database.professor_repository import SQLAlchemyProfessorRepository
from professors.core.ports.professor_repository_port import ProfessorRepositoryPort
from professors.core.services.professor_service import ProfessorService

from professors.adapters.database.graduation_repository import SQLAlchemyGraduationRepository
from professors.core.ports.graduation_repository_port import GraduationRepositoryPort
from professors.core.services.graduation_service import GraduationService

# --- Providers para Professor ---
def get_professor_repository(db: Session = Depends(get_db)) -> ProfessorRepositoryPort:
    return SQLAlchemyProfessorRepository(db)

def get_professor_service(
    repo: ProfessorRepositoryPort = Depends(get_professor_repository)
) -> ProfessorService:
    return ProfessorService(repo)

# --- Providers para Graduation (NOVOS) ---
def get_graduation_repository(db: Session = Depends(get_db)) -> GraduationRepositoryPort:
    return SQLAlchemyGraduationRepository(db)

def get_graduation_service(
    repo: GraduationRepositoryPort = Depends(get_graduation_repository)
) -> GraduationService:
    return GraduationService(repo)
