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
def graduation_service(mock_repo):
    """
    Instância do serviço com repositório mockado.
    O construtor do GraduationService (core/services/graduation_service.py)
    recebe apenas 'repository'.
    """
    return GraduationService(repository=mock_repo)

# --- Test Cases ---

def test_create_graduation_success(graduation_service, mock_repo):
    # Arrange
    grad_create = GraduationCreate(**fake_graduation_data)
    mock_repo.add.return_value = fake_graduation

    # Act
    result = graduation_service.create_graduation(fake_professor_id, grad_create)

    # Assert
    # Verifica se o repositório foi chamado com os argumentos corretos
    mock_repo.add.assert_called_with(fake_professor_id, grad_create)
    assert result.degree == "Mestrado"
    assert result.id == fake_graduation_id

def test_get_all_graduations_for_professor(graduation_service, mock_repo):
    # Arrange
    # O nome do método no serviço é get_all_for_professor
    mock_repo.get_all_for_professor.return_value = [fake_graduation]

    # Act
    result = graduation_service.get_all_graduations_for_professor(fake_professor_id)

    # Assert
    mock_repo.get_all_for_professor.assert_called_with(fake_professor_id)
    assert len(result) == 1
    assert result[0].id == fake_graduation_id

def test_get_all_graduations(graduation_service, mock_repo):
    # Arrange
    mock_repo.get_all.return_value = [fake_graduation]
    
    # Act
    result = graduation_service.get_all_graduations()
    
    # Assert
    mock_repo.get_all.assert_called_once()
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
    # O repositório deve retornar o objeto atualizado
    updated_graduation = Graduation(id=fake_graduation_id, professor_id=fake_professor_id, **grad_update.model_dump())
    mock_repo.update.return_value = updated_graduation

    # Act
    result = graduation_service.update_graduation(fake_graduation_id, grad_update)

    # Assert
    # O serviço passa o objeto Pydantic 'grad_update', não um dict
    mock_repo.update.assert_called_with(fake_graduation_id, grad_update)
    assert result
    assert result.id == fake_graduation_id

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