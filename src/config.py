from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    WEBHOOK_HOST: str 
    BOT_TOKEN: str 
    API_URL: str


    class Config:
        env_file = '.env'


settings = Settings()