from fastapi import FastAPI
from common.data_layer import cargar_cities

app = FastAPI()

@app.get("/api/cities")
def obtener_cities():
    df = cargar_cities()
    return df.to_dict(orient="records")

