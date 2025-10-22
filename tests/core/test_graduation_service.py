import uuid
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from professors.core.services.graduation_service import GraduationService
from professors.core.domain.graduation_models import Graduation, GraduationCreate, GraduationUpdate

# Dados de exemplo
fake_professor_id = uuid.uuid4()
fake_graduation_id = uuid.uuid4()
fake_graduation_data = {
    "degree": "Mestrado",
    "course": "Engenharia de Software",
    "institution_name": "PUCRS",
    "year": 2025
}
fake_graduation = Graduation(
    id=fake_graduation_id, 
    professor_id=fake_professor_id, 
    **fake_graduation_data
)

@pytest.fixture
def mock_repo():
    """Mock do GraduationRepositoryPort."""
    return MagicMock()

@pytest.fixture
def mock_professor_repo():
    """Mock do ProfessorRepositoryPort (necessário para o construtor)."""
    return MagicMock()

@pytest.fixture
def graduation_service(mock_repo, mock_professor_repo):
    """Instância do serviço com repositórios mockados."""
    # Assumindo que o serviço de professor (ou seu repo) é injetado
    # Se o construtor for diferente, ajuste aqui.
    # Baseado no dependencies.py, ele recebe ProfessorRepository e GraduationRepository
    return GraduationService(
        professor_repository=mock_professor_repo, 
        graduation_repository=mock_repo
    )

# --- Test Cases ---

def test_add_graduation_to_professor_success(graduation_service, mock_repo, mock_professor_repo):
    # Arrange
    grad_create = GraduationCreate(**fake_graduation_data)
    mock_professor_repo.get_by_id.return_value = True # Simula que o professor existe
    mock_repo.add.return_value = fake_graduation
    
    # Act
    result = graduation_service.add_graduation_to_professor(fake_professor_id, grad_create)
    
    # Assert
    mock_professor_repo.get_by_id.assert_called_with(fake_professor_id)
    mock_repo.add.assert_called_with(grad_create, fake_professor_id)
    assert result.degree == "Mestrado"

def test_add_graduation_to_professor_not_found(graduation_service, mock_repo, mock_professor_repo):
    # Arrange
    grad_create = GraduationCreate(**fake_graduation_data)
    mock_professor_repo.get_by_id.return_value = None # Professor não existe
    
    # Act / Assert
    with pytest.raises(HTTPException) as exc_info:
        graduation_service.add_graduation_to_professor(fake_professor_id, grad_create)
    
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    mock_repo.add.assert_not_called()

def test_get_graduations_by_professor_id(graduation_service, mock_repo):
    # Arrange
    mock_repo.get_by_professor_id.return_value = [fake_graduation]
    
    # Act
    result = graduation_service.get_graduations_by_professor_id(fake_professor_id)
    
    # Assert
    mock_repo.get_by_professor_id.assert_called_with(fake_professor_id)
    assert len(result) == 1
    assert result[0].id == fake_graduation_id

def test_get_graduation_by_id_success(graduation_service, mock_repo):
    # Arrange
    mock_repo.get_by_id.return_value = fake_graduation
    
    # Act
    result = graduation_service.get_graduation_by_id(fake_graduation_id)
    
    # Assert
    mock_repo.get_by_id.assert_called_with(fake_graduation_id)
    assert result.id == fake_graduation_id

def test_get_graduation_by_id_not_found(graduation_service, mock_repo):
    # Arrange
    mock_repo.get_by_id.return_value = None
    
    # Act / Assert
    with pytest.raises(HTTPException) as exc_info:
        graduation_service.get_graduation_by_id(uuid.uuid4())
    
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

def test_update_graduation_success(graduation_service, mock_repo):
    # Arrange
    grad_update = GraduationUpdate(**fake_graduation_data)
    mock_repo.update.return_value = fake_graduation
    
    # Act
    result = graduation_service.update_graduation(fake_graduation_id, grad_update)
    
    # Assert
    mock_repo.update.assert_called_with(fake_graduation_id, grad_update.model_dump())
    assert result

def test_update_graduation_not_found(graduation_service, mock_repo):
    # Arrange
    grad_update = GraduationUpdate(**fake_graduation_data)
    mock_repo.update.return_value = None
    
    # Act / Assert
    with pytest.raises(HTTPException) as exc_info:
        graduation_service.update_graduation(fake_graduation_id, grad_update)
    
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

def test_delete_graduation_success(graduation_service, mock_repo):
    # Arrange
    mock_repo.delete.return_value = True
    
    # Act
    graduation_service.delete_graduation(fake_graduation_id)
    
    # Assert
    mock_repo.delete.assert_called_with(fake_graduation_id)

def test_delete_graduation_not_found(graduation_service, mock_repo):
    # Arrange
    mock_repo.delete.return_value = False
    
    # Act / Assert
    with pytest.raises(HTTPException) as exc_info:
        graduation_service.delete_graduation(fake_graduation_id)
    
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND