import os

from dotenv import load_dotenv

# from pydantic_settings import BaseSettings, SettingsConfigDict

# try:
# except Exception as e:
#     print(f'An exception occurred {e}')


class Settings:
    # model_config = SettingsConfigDict(validate_default=False)

    load_env = load_dotenv(".env")
    if not load_env:
        load_env = load_dotenv("Docker.env")
    # Setting read Hasing config
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    # settings of the docker-compose
    PROJECT_NAME: str = "backend-alternova"
    PROJECT_VERSION: str = "0.1"
    # Postgres conexion
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    # DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    # print(DATABASE_URL)


settings = Settings()
