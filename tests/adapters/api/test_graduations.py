import uuid
from fastapi import status, HTTPException
from professors.core.domain.graduation_models import Graduation, GraduationCreate

# Mock de dados
fake_professor_id = uuid.uuid4()
fake_graduation_id = uuid.uuid4()
fake_graduation_request = {
    "degree": "Mestrado",
    "course": "Engenharia de Software",
    "institution_name": "PUCRS",
    "year": 2025
}

# Objeto de modelo Pydantic para o response (Corrige ResponseValidationError)
fake_graduation_response_model = Graduation(
    id=fake_graduation_id,
    professor_id=fake_professor_id,
    **fake_graduation_request
)


def test_create_graduation_success(client, mock_graduation_service, mock_professor_service):
    # Arrange
    # A rota valida o professor primeiro (mock_professor_service)
    mock_professor_service.get_professor_by_id.return_value = {"id": fake_professor_id} 
    # O serviço de graduação é chamado e retorna o modelo Pydantic
    mock_graduation_service.create_graduation.return_value = fake_graduation_response_model

    # Act
    response = client.post(
        f"/api/v1/professors/{fake_professor_id}/graduations/",
        json=fake_graduation_request
    )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] == str(fake_graduation_id) # O JSON serializa UUIDs para strings
    # Verifica se o mock foi chamado com os dados corretos
    mock_graduation_service.create_graduation.assert_called_once_with(
        fake_professor_id,
        GraduationCreate(**fake_graduation_request) # O serviço espera um objeto GraduationCreate
    )

def test_create_graduation_professor_not_found(client, mock_professor_service):
    # Arrange
    # Simula o 'get_professor' (dependência da rota) falhando
    mock_professor_service.get_professor_by_id.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Professor not found."
    )

    # Act
    response = client.post(
        f"/api/v1/professors/{fake_professor_id}/graduations/",
        json=fake_graduation_request
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_graduations_for_professor(client, mock_graduation_service, mock_professor_service):
    # Arrange
    mock_professor_service.get_professor_by_id.return_value = {"id": fake_professor_id}
    mock_graduation_service.get_all_graduations_for_professor.return_value = [fake_graduation_response_model]

    # Act
    response = client.get(f"/api/v1/professors/{fake_professor_id}/graduations/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["degree"] == "Mestrado"
    mock_graduation_service.get_all_graduations_for_professor.assert_called_with(fake_professor_id)


def test_get_all_graduations(client, mock_graduation_service):
    # Arrange
    mock_graduation_service.get_all_graduations.return_value = [fake_graduation_response_model]
    
    # Act
    response = client.get("/api/v1/graduations/")
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == str(fake_graduation_id)


def test_update_graduation_success(client, mock_graduation_service, mock_professor_service):
    # Arrange
    mock_professor_service.get_professor_by_id.return_value = {"id": fake_professor_id}
    # O mock de update deve retornar o objeto atualizado
    mock_graduation_service.update_graduation.return_value = fake_graduation_response_model

    # Act
    # A rota correta é a aninhada
    response = client.put(
        f"/api/v1/professors/{fake_professor_id}/graduations/{fake_graduation_id}", 
        json=fake_graduation_request
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["course"] == "Engenharia de Software"
    mock_graduation_service.update_graduation.assert_called_once()

def test_delete_graduation_success(client, mock_graduation_service, mock_professor_service):
    # Arrange
    mock_professor_service.get_professor_by_id.return_value = {"id": fake_professor_id}
    mock_graduation_service.delete_graduation.return_value = None

    # Act
    # A rota correta é a aninhada
    response = client.delete(
        f"/api/v1/professors/{fake_professor_id}/graduations/{fake_graduation_id}"
    )

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    mock_graduation_service.delete_graduation.assert_called_with(fake_graduation_id)