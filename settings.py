from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+psycopg2://postgres:1234@localhost:5544/client_data?options=-csearch_path%3Ddbo,public"
    CLIENT_DATASET_PATH: str = 'backend/data/client_dataset.csv'


