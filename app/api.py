from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

# Crear el engine de conexión a PostgreSQL
engine = create_engine(
    "postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data"
)


