from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PG_HOST: str
    PG_USER: str
    PG_PASSWORD: str
    PG_DATABASE_NAME: str

    JWT_SECRET_KEY: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()