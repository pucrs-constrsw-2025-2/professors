import uuid
from fastapi import status, HTTPException

# Mock de dados
fake_professor_id = str(uuid.uuid4())
fake_graduation_id = str(uuid.uuid4())
fake_graduation_request = {
    "degree": "Mestrado",
    "course": "Engenharia de Software",
    "institution_name": "PUCRS",
    "year": 2025
}
fake_graduation_response = {
    "id": fake_graduation_id,
    "professor_id": fake_professor_id,
    **fake_graduation_request
}

def test_create_graduation_success(client, mock_graduation_service):
    # Arrange
    mock_graduation_service.add_graduation_to_professor.return_value = fake_graduation_response
    
    # Act
    response = client.post(
        f"/api/v1/professors/{fake_professor_id}/graduations/", 
        json=fake_graduation_request
    )
    
    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] == fake_graduation_id
    mock_graduation_service.add_graduation_to_professor.assert_called_once()

def test_create_graduation_professor_not_found(client, mock_graduation_service):
    # Arrange
    mock_graduation_service.add_graduation_to_professor.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Professor not found."
    )
    
    # Act
    response = client.post(
        f"/api/v1/professors/{fake_professor_id}/graduations/", 
        json=fake_graduation_request
    )
    
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_graduations_for_professor(client, mock_graduation_service):
    # Arrange
    mock_graduation_service.get_graduations_by_professor_id.return_value = [fake_graduation_response]
    
    # Act
    response = client.get(f"/api/v1/professors/{fake_professor_id}/graduations/")
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["degree"] == "Mestrado"

def test_get_single_graduation_success(client, mock_graduation_service):
    # Arrange
    mock_graduation_service.get_graduation_by_id.return_value = fake_graduation_response
    
    # Act
    response = client.get(f"/api/v1/graduations/{fake_graduation_id}")
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == fake_graduation_id

def test_get_single_graduation_not_found(client, mock_graduation_service):
    # Arrange
    mock_graduation_service.get_graduation_by_id.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )
    
    # Act
    response = client.get(f"/api/v1/graduations/{fake_graduation_id}")
    
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_graduation_success(client, mock_graduation_service):
    # Arrange
    mock_graduation_service.update_graduation.return_value = fake_graduation_response
    
    # Act
    response = client.put(f"/api/v1/graduations/{fake_graduation_id}", json=fake_graduation_request)
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["course"] == "Engenharia de Software"

def test_delete_graduation_success(client, mock_graduation_service):
    # Arrange
    mock_graduation_service.delete_graduation.return_value = None
    
    # Act
    response = client.delete(f"/api/v1/graduations/{fake_graduation_id}")
    
    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT