from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    JWT_SECRET: str
    OPENAI_API_KEY: str
    WHISPER_MODEL: str = "small"
    REACT_APP_API_BASE: str

    class Config:
        env_file = "../.env"

settings = Settings()