from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    # Configurações do serviço Professors
    PROFESSORS_INTERNAL_API_PORT: int = 8082
        
    # Configurações do Banco de Dados (lidas do .env principal)
    POSTGRESQL_USERNAME: str = Field(..., env="POSTGRESQL_USERNAME")
    POSTGRESQL_PASSWORD: str = Field(..., env="POSTGRESQL_PASSWORD")
    POSTGRESQL_INTERNAL_HOST: str = Field(..., env="POSTGRESQL_INTERNAL_HOST")
    POSTGRESQL_INTERNAL_PORT: int = Field(..., env="POSTGRESQL_INTERNAL_PORT")
    
    # DB Específico para este microsserviço (recomendo adicionar ao .env)
    PROFESSORS_POSTGRESQL_DB: str = Field("professors", env="PROFESSORS_POSTGRESQL_DB")

    @property
    def DATABASE_URL(self) -> str:
        """URL de conexão com o banco de dados SQLAlchemy."""
        return (
            f"postgresql+psycopg2://{self.POSTGRESQL_USERNAME}:{self.POSTGRESQL_PASSWORD}@"
            f"{self.POSTGRESQL_INTERNAL_HOST}:{self.POSTGRESQL_INTERNAL_PORT}/"
            f"{self.PROFESSORS_POSTGRESQL_DB}"
        )

    class Config:
        env_file = "../../.env"
        env_file_encoding = "utf-8"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()