from fastapi import FastAPI
from fastapi import Query
from datetime import datetime
from common.data_layer import cargar_cities
import common.data_layer_c as data_layer_c

app = FastAPI()

@app.get("/api/cities")
def obtener_cities():
    df = cargar_cities()
    return df.to_dict(orient="records")

@app.get("/api/state_borders")
def obtener_estado_fronteras():
    df = data_layer_c.estado_fronteras()
    return df.to_dict(orient="records")

@app.get("/api/city_borders")
def obtener_ciudad_fronteras():
    df = data_layer_c.ciudad_fronteras()
    return df.to_dict(orient="records")

@app.get("/api/parcels")
def obtener_parcelas():
    df = data_layer_c.parcels()
    return df.to_dict(orient="records")

@app.get("/api/roads")
def obtener_carreteras():
    df = data_layer_c.roads()
    return df.to_dict(orient="records")

@app.get("/api/rental_vehicles")
def obtener_vehiculos_de_alquiler():
    df = data_layer_c.rental_vehicles()
    return df.to_dict(orient="records")

@app.get("/api/greenlake-eval/test")
def ping():
    return {
        "metadata": {
            "status": "success",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        },
        "results": {
            "status": "active"
        }
    }
     