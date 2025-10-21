import uuid
from sqlalchemy import Column, String, Uuid, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Professor(Base):
    """Modelo da tabela Professors no banco de dados."""
    
    __tablename__ = "professors"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    registration_number = Column(Integer, unique=True, index=True, nullable=False)
    institucional_email = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, nullable=False, default="active")

    # Relacionamento com Graduation
    graduations = relationship("Graduation", back_populates="professor", cascade="all, delete-orphan")

class Graduation(Base):
    """Modelo da tabela Graduations no banco de dados."""
    
    __tablename__ = "graduations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    degree = Column(String, nullable=False)
    course = Column(String, nullable=False)
    institution_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    professor_id = Column(Uuid(as_uuid=True), ForeignKey("professors.id"), nullable=False)
    professor = relationship("Professor", back_populates="graduations")
