from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

# Instantiate settings object which will read from the .env file
settings = Settings()
