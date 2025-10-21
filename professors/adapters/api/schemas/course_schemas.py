import uuid
from pydantic import BaseModel, Field

# Exemplo de resposta para GET /professors/{{id}}/courses
class CourseResponse(BaseModel):
    id: uuid.UUID
    name: str
    # ... outros dados do curso