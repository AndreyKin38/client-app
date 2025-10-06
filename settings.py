from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_DRIVER: str = 'postgresql+psycopg2'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5544
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = '1234'
    DB_NAME: str = 'client_data'

    CACHE_HOST: str = 'localhost'
    CACHE_PORT: int = 6379
    CACHE_DB: int | str = 0

    CLIENT_DATASET_PATH: str = 'backend/data/client_dataset.csv'

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'




