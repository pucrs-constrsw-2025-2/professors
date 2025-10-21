import uuid
from sqlalchemy import Column, String, Uuid, Integer
from .database import Base

class Professor(Base):
    """Modelo da tabela Professors no banco de dados."""
    
    __tablename__ = "professors"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    name = Column(String, nullable=False)
    
    registration_number = Column(Integer, unique=True, index=True, nullable=False)
    
    institucional_email = Column(String, unique=True, index=True, nullable=False)
    
    status = Column(String, nullable=False, default="active")