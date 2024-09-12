from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:NewSecurePassword123@localhost:3306/bootstrap_db"

    class Config:
        env_file = ".env"

settings = Settings()
