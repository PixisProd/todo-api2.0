from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PG_HOST: str = "localhost"
    PG_USER: str = "postgres"
    PG_PASSWORD: str
    PG_DATABASE_NAME: str
    PG_TEST_DATABASE_NAME: str

    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_COOKIE_NAME: str
    JWT_REFRESH_TOKEN_COOKIE_NAME: str
    JWT_ALGORITHM: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()