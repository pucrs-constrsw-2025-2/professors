import uuid
from sqlalchemy import Column, String, Uuid
from .database import Base

class Professor(Base):
    """Modelo da tabela Professors no banco de dados."""
    
    __tablename__ = "professors"

    # _id (PK) conforme resposta do message.txt [cite: 5]
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # id_professor (lógica de negócio) [cite: 2]
    id_professor = Column(String, unique=True, index=True, nullable=False)
    
    name = Column(String, nullable=False)
    
    # registration_number (lógica de negócio) [cite: 2]
    registration_number = Column(String, unique=True, index=True, nullable=False)
    
    institucional_email = Column(String, unique=True, index=True, nullable=False)
    
    status = Column(String, nullable=False, default="active")