import uuid
from pydantic import BaseModel, Field

# Exemplo de resposta para GET /professors/{{id}}/lessons
class LessonResponse(BaseModel):
    id: uuid.UUID
    topic: str
    date: str # Ou datetime
    # ... outros dados da aula