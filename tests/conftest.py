import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from professors.main import app
# Importar o novo serviço
from professors.dependencies import get_professor_service, get_graduation_service
from professors.adapters.api.auth import validate_token

# Fixture para o mock do serviço (lógica de negócio)
@pytest.fixture
def mock_professor_service():
    """Retorna um mock do ProfessorService."""
    return MagicMock()

# --- NOVO FIXTURE ---
@pytest.fixture
def mock_graduation_service():
    """Retorna um mock do GraduationService."""
    return MagicMock()

# Fixture para o cliente da API
@pytest.fixture
def client(mock_professor_service, mock_graduation_service): # <-- Adicionar mock
    """Retorna um TestClient da API com dependências mockadas."""
    
    # 1. Mockar a autenticação (essencial)
    app.dependency_overrides[validate_token] = lambda: {"sub": "test-user-id"}
    
    # 2. Mockar os serviços (para testar as rotas em isolamento)
    app.dependency_overrides[get_professor_service] = lambda: mock_professor_service
    app.dependency_overrides[get_graduation_service] = lambda: mock_graduation_service # <-- Adicionar
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Limpa os overrides após os testes
    app.dependency_overrides = {}