# tests/test_main.py
from fastapi import status

def test_health_check(client):
    # Arrange
    # (client fixture é usado)
    
    # Act
    response = client.get("/health")
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}

# Nota: Testar o 'lifespan' (criação de tabelas) é mais complexo.
# Para 100% de coverage, você pode mockar 'asyncio.to_thread' e 'Base.metadata.create_all'
# e verificar se são chamados durante a inicialização do TestClient.