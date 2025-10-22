# tests/adapters/api/test_professors.py
import uuid
from fastapi import status, HTTPException

# Mock de dados (completo)
fake_professor_id = str(uuid.uuid4())
fake_professor_create_request = {
    "name": "Dr. Test",
    "registration_number": 12345,
    "institucional_email": "test@pucrs.br",
    "status": "active"
}
fake_professor_response = {
    "id": fake_professor_id,
    **fake_professor_create_request
}

# --- Test Cases ---

def test_create_professor_success(client, mock_professor_service):
    # Arrange
    mock_professor_service.create_professor.return_value = fake_professor_response
    
    # Act
    response = client.post("/api/v1/professors/", json=fake_professor_create_request)
    
    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Dr. Test"
    mock_professor_service.create_professor.assert_called_once()

def test_create_professor_handles_service_conflict(client, mock_professor_service):
    # Arrange
    mock_professor_service.create_professor.side_effect = HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="Conflict"
    )
    
    # Act
    response = client.post("/api/v1/professors/", json=fake_professor_create_request)
    
    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Conflict"

def test_create_professor_handles_generic_exception(client, mock_professor_service):
    # Arrange
    mock_professor_service.create_professor.side_effect = Exception("Generic Error")
    
    # Act
    response = client.post("/api/v1/professors/", json=fake_professor_create_request)
    
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_search_professors_no_params(client, mock_professor_service):
    # Arrange
    mock_professor_service.get_all_professors.return_value = [fake_professor_response]
    
    # Act
    response = client.get("/api/v1/professors/")
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    mock_professor_service.get_all_professors.assert_called_once()
    mock_professor_service.search_professors.assert_not_called()

def test_search_professors_with_params(client, mock_professor_service):
    # Arrange
    mock_professor_service.search_professors.return_value = [fake_professor_response]
    
    # Act
    response = client.get("/api/v1/professors/?name=Test&status=active")
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    mock_professor_service.search_professors.assert_called_with({"name": "Test", "status": "active"})
    mock_professor_service.get_all_professors.assert_not_called()

def test_get_professor_success(client, mock_professor_service):
    # Arrange
    mock_professor_service.get_professor_by_id.return_value = fake_professor_response
    
    # Act
    response = client.get(f"/api/v1/professors/{fake_professor_id}")
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == fake_professor_id

def test_get_professor_not_found(client, mock_professor_service):
    # Arrange
    prof_id = str(uuid.uuid4())
    mock_professor_service.get_professor_by_id.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Professor not found."
    )
    
    # Act
    response = client.get(f"/api/v1/professors/{prof_id}")
    
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_professor_success(client, mock_professor_service):
    # Arrange
    update_data = {
        "name": "Updated",
        "registration_number": 123,
        "institucional_email": "updated@pucrs.br",
        "status": "inactive"
    }
    mock_professor_service.update_professor.return_value = {"id": fake_professor_id, **update_data}
    
    # Act
    response = client.put(f"/api/v1/professors/{fake_professor_id}", json=update_data)
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated"

def test_delete_professor_success(client, mock_professor_service):
    # Arrange
    prof_id = str(uuid.uuid4())
    mock_professor_service.delete_professor.return_value = None
    
    # Act
    response = client.delete(f"/api/v1/professors/{prof_id}")
    
    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    mock_professor_service.delete_professor.assert_called_with(uuid.UUID(prof_id))