import uuid
from pydantic import BaseModel, Field

# Exemplo de resposta para GET /professors/{{id}}/classes
class ClassResponse(BaseModel):
    id: uuid.UUID
    name: str
    semester: str
    # ... outros dados da classe

# Request body para POST /professors/{{id}}/classes
class AssociateClassRequest(BaseModel):
    class_id: uuid.UUID