from fastapi import APIRouter, status
from typing import List

from ..schemas.professor_schemas import Professor, ProfessorCreate, ProfessorUpdate

router = APIRouter()

@router.post("/", response_model=Professor, status_code=status.HTTP_201_CREATED)
async def create_professor(professor: ProfessorCreate):
    """
    Create a new professor.
    """
    return {"id": 1, **professor.dict()}

@router.get("/", response_model=List[Professor])
async def get_professors():
    """
    Get all professors.
    """
    return [
        {"id": 1, "name": "Dr. Smith", "email": "smith@example.com", "department": "Computer Science"},
        {"id": 2, "name": "Dr. Jones", "email": "jones@example.com", "department": "Physics"},
    ]

@router.get("/{professor_id}", response_model=Professor)
async def get_professor(professor_id: int):
    """
    Get a single professor by ID.
    """
    return {"id": professor_id, "name": "Dr. Smith", "email": "smith@example.com", "department": "Computer Science"}

@router.put("/{professor_id}", response_model=Professor)
async def update_professor(professor_id: int, professor: ProfessorUpdate):
    """
    Update a professor.
    """
    return {"id": professor_id, "name": "Dr. Smith", "email": "smith@example.com", "department": "Computer Science", **professor.dict(exclude_unset=True)}

@router.delete("/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_professor(professor_id: int):
    """
    Delete a professor.
    """
    return
