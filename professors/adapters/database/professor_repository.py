import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from professors.core.ports.professor_repository_port import ProfessorRepositoryPort
from professors.core.domain.professor_models import Professor, ProfessorCreate, ProfessorUpdate
from .models import Professor as ProfessorTableModel # Model da tabela

class SQLAlchemyProfessorRepository(ProfessorRepositoryPort):
    
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, db_professor: ProfessorTableModel) -> Professor:
        """Converte o modelo SQLAlchemy para o modelo de domínio Pydantic."""
        if db_professor is None:
            return None
        
        # Passar o __dict__ contorna o problema do Pydantic v2 (from_attributes=True)
        # ignorar atributos que começam com '_', como o nosso '_id'.
        # Ao passar um dict, Pydantic usará o alias '_id' para preencher 'db_id'.
        return Professor.model_validate(db_professor.__dict__)

    def add(self, professor_data: ProfessorCreate) -> Professor:
        try:
            db_professor = ProfessorTableModel(**professor_data.model_dump())
            self.db.add(db_professor)
            self.db.commit()
            self.db.refresh(db_professor)
            return self._to_domain(db_professor)
        except IntegrityError as e:
            self.db.rollback()
            # Isso é um fallback, o serviço já deve ter verificado
            raise ValueError(f"Database integrity error: {e.orig}")

    def get_by_id(self, professor_uuid: uuid.UUID) -> Optional[Professor]:
        db_professor = self.db.query(ProfessorTableModel).filter(ProfessorTableModel._id == professor_uuid).first()
        return self._to_domain(db_professor) if db_professor else None

    def get_by_id_professor(self, id_professor: str) -> Optional[Professor]:
        db_professor = self.db.query(ProfessorTableModel).filter(ProfessorTableModel.id_professor == id_professor).first()
        return self._to_domain(db_professor) if db_professor else None

    def get_by_registration_number(self, reg_number: str) -> Optional[Professor]:
        db_professor = self.db.query(ProfessorTableModel).filter(ProfessorTableModel.registration_number == reg_number).first()
        return self._to_domain(db_professor) if db_professor else None

    def get_all(self) -> List[Professor]:
        db_professors = self.db.query(ProfessorTableModel).all()
        return [self._to_domain(p) for p in db_professors]
    
    def search(self, params: Dict[str, Any]) -> List[Professor]:
        query = self.db.query(ProfessorTableModel)
        
        if "name" in params:
            query = query.filter(ProfessorTableModel.name.ilike(f"%{params['name']}%"))
        if "status" in params:
            query = query.filter(ProfessorTableModel.status == params['status'])
        # Adicione outros filtros conforme necessário
            
        db_professors = query.all()
        return [self._to_domain(p) for p in db_professors]

    def update(self, professor_uuid: uuid.UUID, professor_data: Dict[str, Any]) -> Optional[Professor]:
        db_professor = self.db.query(ProfessorTableModel).filter(ProfessorTableModel._id == professor_uuid).first()
        
        if not db_professor:
            return None
        
        # Atualiza apenas os campos fornecidos
        for key, value in professor_data.items():
            if value is not None: # Importante para PATCH
                setattr(db_professor, key, value)
        
        try:
            self.db.commit()
            self.db.refresh(db_professor)
            return self._to_domain(db_professor)
        except IntegrityError:
            self.db.rollback()
            return None # Ou levanta uma exceção de conflito

    def delete(self, professor_uuid: uuid.UUID) -> bool:
        db_professor = self.db.query(ProfessorTableModel).filter(ProfessorTableModel._id == professor_uuid).first()
        
        if db_professor:
            self.db.delete(db_professor)
            self.db.commit()
            return True
        return False