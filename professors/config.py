from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    # Configurações do Banco de Dados (lidas do .env principal)
    POSTGRESQL_USERNAME: str = Field(..., env="POSTGRESQL_USERNAME")
    POSTGRESQL_PASSWORD: str = Field(..., env="POSTGRESQL_PASSWORD")
    POSTGRESQL_INTERNAL_HOST: str = Field(..., env="POSTGRESQL_INTERNAL_HOST")
    POSTGRESQL_INTERNAL_PORT: int = Field(..., env="POSTGRESQL_INTERNAL_PORT")
    
    PROFESSORS_POSTGRESQL_DB: str = Field(..., env="PROFESSORS_POSTGRESQL_DB")

    OAUTH_INTERNAL_PROTOCOL: str = Field(..., env="OAUTH_INTERNAL_PROTOCOL")
    OAUTH_INTERNAL_HOST: str = Field(..., env="OAUTH_INTERNAL_HOST")
    OAUTH_INTERNAL_API_PORT: int = Field(..., env="OAUTH_INTERNAL_API_PORT")

    @property
    def DATABASE_URL(self) -> str:
        """URL de conexão com o banco de dados SQLAlchemy."""
        return (
            f"postgresql+psycopg2://{self.POSTGRESQL_USERNAME}:{self.POSTGRESQL_PASSWORD}@"
            f"{self.POSTGRESQL_INTERNAL_HOST}:{self.POSTGRESQL_INTERNAL_PORT}/"
            f"{self.PROFESSORS_POSTGRESQL_DB}"
        )

    @property
    def OAUTH_VALIDATE_URL(self) -> str:
        """URL completa para o endpoint de validação de token."""
        return f"{self.OAUTH_INTERNAL_PROTOCOL}://{self.OAUTH_INTERNAL_HOST}:{self.OAUTH_INTERNAL_API_PORT}/validate"

    class Config:
        env_file = "../../.env"
        env_file_encoding = "utf-8"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()