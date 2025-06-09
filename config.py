import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        # Configurações do PostgreSQL usando variáveis de ambiente
        db_host = os.getenv("POSTGRES_HOST")
        db_port = os.getenv("POSTGRES_PORT")
        db_name = os.getenv("POSTGRES_DB")
        db_user = os.getenv("POSTGRES_USER")
        db_password = os.getenv("POSTGRES_PASSWORD")

        # Construir a URL do banco de dados
        self.SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

