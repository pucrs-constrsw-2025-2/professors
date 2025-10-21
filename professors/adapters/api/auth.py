from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # <-- ALTERADO
import httpx

from professors.config import settings

# Usamos HTTPBearer em vez de OAuth2PasswordBearer.
# Isso dirá ao Swagger para pedir apenas o token, não usuário/senha.
http_bearer_scheme = HTTPBearer()

async def validate_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer_scheme)]):
    """
    Dependência que valida o token de portador (Bearer Token) com o serviço de OAuth.
    Extrai o token do esquema HTTPBearer.
    """
    token = credentials.credentials
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        try:
            # Chama o endpoint /validate do serviço de OAuth
            response = await client.post(settings.OAUTH_VALIDATE_URL, headers=headers)
            
            # Se a resposta for 4xx ou 5xx, levanta uma exceção
            response.raise_for_status()
            
            # Retorna os dados da introspecção do token se for válido
            return response.json()

        except httpx.HTTPStatusError as exc:
            # Captura erros 4xx/5xx (ex: 401 do serviço oauth)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except httpx.RequestError:
            # Captura erros de rede (ex: serviço oauth indisponível)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de autenticação indisponível.",
            )

