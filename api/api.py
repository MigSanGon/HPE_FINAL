from fastapi import FastAPI
from typing import Optional
from common.data_layer import cargar_people_enriquecido

app = FastAPI()

@app.get("/api/greenlake-eval/people")
def obtener_people(skip: int = 0, limit: int = 100):
    df = cargar_people_enriquecido(skip=skip, limit=limit)
    return df.to_dict(orient="records")
