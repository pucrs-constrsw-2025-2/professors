import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from professors.core.domain.graduation_models import Graduation, GraduationCreate, GraduationUpdate
from professors.core.ports.graduation_repository_port import GraduationRepositoryPort
from .models import Graduation as GraduationTableModel

class SQLAlchemyGraduationRepository(GraduationRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, db_graduation: GraduationTableModel) -> Graduation:
        return Graduation.model_validate(db_graduation)

    def add(self, professor_id: uuid.UUID, graduation_data: GraduationCreate) -> Graduation:
        db_graduation = GraduationTableModel(
            **graduation_data.model_dump(),
            professor_id=professor_id
        )
        self.db.add(db_graduation)
        self.db.commit()
        self.db.refresh(db_graduation)
        return self._to_domain(db_graduation)

    def get_by_id(self, graduation_id: uuid.UUID) -> Optional[Graduation]:
        db_graduation = self.db.query(GraduationTableModel).filter(GraduationTableModel.id == graduation_id).first()
        return self._to_domain(db_graduation) if db_graduation else None

    def get_all_for_professor(self, professor_id: uuid.UUID) -> List[Graduation]:
        db_graduations = self.db.query(GraduationTableModel).filter(GraduationTableModel.professor_id == professor_id).all()
        return [self._to_domain(g) for g in db_graduations]

    # NOVO MÉTODO
    def get_all(self) -> List[Graduation]:
        db_graduations = self.db.query(GraduationTableModel).all()
        return [self._to_domain(g) for g in db_graduations]

    def update(self, graduation_id: uuid.UUID, graduation_data: GraduationUpdate) -> Optional[Graduation]:
        db_graduation = self.db.query(GraduationTableModel).filter(GraduationTableModel.id == graduation_id).first()
        if not db_graduation:
            return None
        
        update_data = graduation_data.model_dump()
        for key, value in update_data.items():
            setattr(db_graduation, key, value)
            
        self.db.commit()
        self.db.refresh(db_graduation)
        return self._to_domain(db_graduation)

    def delete(self, graduation_id: uuid.UUID) -> bool:
        db_graduation = self.db.query(GraduationTableModel).filter(GraduationTableModel.id == graduation_id).first()
        if db_graduation:
            self.db.delete(db_graduation)
            self.db.commit()
            return True
        return False