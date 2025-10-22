# tests/core/test_professor_service.py
import uuid
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from professors.core.services.professor_service import ProfessorService
from professors.core.domain.professor_models import ProfessorCreate, ProfessorUpdate, Professor

# Dados de exemplo completos
fake_professor_data = {
    "name": "Test User",
    "registration_number": 123,
    "institucional_email": "test@pucrs.br",
    "status": "active"
}
fake_professor_id = uuid.uuid4()
fake_professor = Professor(id=fake_professor_id, **fake_professor_data)

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def professor_service(mock_repo):
    return ProfessorService(repository=mock_repo)

# --- Test Cases ---

def test_create_professor_success(professor_service, mock_repo):
    # Arrange
    professor_data = ProfessorCreate(**fake_professor_data)
    mock_repo.get_by_registration_number.return_value = None
    mock_repo.add.return_value = fake_professor
    
    # Act
    result = professor_service.create_professor(professor_data)
    
    # Assert
    mock_repo.get_by_registration_number.assert_called_with(123)
    mock_repo.add.assert_called_with(professor_data)
    assert result.name == "Test User"

def test_create_professor_conflict_raises_http_409(professor_service, mock_repo):
    # Arrange
    professor_data = ProfessorCreate(**fake_professor_data)
    mock_repo.get_by_registration_number.return_value = fake_professor
    
    # Act / Assert
    with pytest.raises(HTTPException) as exc_info:
        professor_service.create_professor(professor_data)
        
    assert exc_info.value.status_code == status.HTTP_409_CONFLICT
    mock_repo.add.assert_not_called()

def test_get_professor_by_id_success(professor_service, mock_repo):
    # Arrange
    mock_repo.get_by_id.return_value = fake_professor
    
    # Act
    result = professor_service.get_professor_by_id(fake_professor_id)
    
    # Assert
    mock_repo.get_by_id.assert_called_with(fake_professor_id)
    assert result.id == fake_professor_id

def test_get_professor_by_id_not_found_raises_http_404(professor_service, mock_repo):
    # Arrange
    prof_id = uuid.uuid4()
    mock_repo.get_by_id.return_value = None
    
    # Act / Assert
    with pytest.raises(HTTPException) as exc_info:
        professor_service.get_professor_by_id(prof_id)
        
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

def test_get_all_professors(professor_service, mock_repo):
    # Arrange
    mock_repo.get_all.return_value = [fake_professor, fake_professor]
    
    # Act
    result = professor_service.get_all_professors()
    
    # Assert
    assert len(result) == 2
    mock_repo.get_all.assert_called_once()

def test_search_professors(professor_service, mock_repo):
    # Arrange
    params = {"name": "Test", "status": "active"}
    mock_repo.search.return_value = [fake_professor]
    
    # Act
    result = professor_service.search_professors(params)
    
    # Assert
    mock_repo.search.assert_called_with(params)
    assert len(result) == 1

def test_update_professor_success(professor_service, mock_repo):
    # Arrange
    update_data_dict = {
        "name": "Updated Name",
        "registration_number": 456,
        "institucional_email": "updated@pucrs.br",
        "status": "inactive"
    }
    update_data = ProfessorUpdate(**update_data_dict)
    mock_repo.update.return_value = Professor(id=fake_professor_id, **update_data_dict)
    
    # Act
    result = professor_service.update_professor(fake_professor_id, update_data)
    
    # Assert
    mock_repo.update.assert_called_with(fake_professor_id, update_data.model_dump())
    assert result.name == "Updated Name"

def test_update_professor_not_found_raises_http_404(professor_service, mock_repo):
    # Arrange
    update_data = ProfessorUpdate(**fake_professor_data)
    mock_repo.update.return_value = None
    
    # Act / Assert
    with pytest.raises(HTTPException) as exc_info:
        professor_service.update_professor(fake_professor_id, update_data)
        
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

def test_delete_professor_success(professor_service, mock_repo):
    # Arrange
    mock_repo.delete.return_value = True
    
    # Act
    professor_service.delete_professor(fake_professor_id)
    
    # Assert
    mock_repo.delete.assert_called_with(fake_professor_id)

def test_delete_professor_not_found_raises_http_404(professor_service, mock_repo):
    # Arrange
    mock_repo.delete.return_value = False
    
    # Act / Assert
    with pytest.raises(HTTPException) as exc_info:
        professor_service.delete_professor(fake_professor_id)
        
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND