from fastapi import FastAPI
from common.data_layer_med import cargar_med,cargar_clin,cargar_phar,cargar_cities1
from common.data_layer_asist import cargar_dayc,cargar_pet,cargar_seni,cargar_event_c,cargar_event_s
from common.data_layer_supply import cargar_gas,cargar_shop,cargar_super,cargar_auto
from common.data_layer_descan import cargar_gym,cargar_venue,cargar_restaurant,cargar_park,cargar_hotel,cargar_religious_building

app = FastAPI()

@app.get("/api/cities")
def obtener_cities():
    df = cargar_cities1()
    return df.to_dict(orient="records")

@app.get("/api/med")
def obtener_med():
    df = cargar_med()
    return df.to_dict(orient="records")

@app.get("/api/clin")
def obtener_clin():
    df = cargar_clin()
    return df.to_dict(orient="records")

@app.get("/api/phar")
def obtener_phar():
    df = cargar_phar()
    return df.to_dict(orient="records")


@app.get("/api/dayc")
def obtener_dayc():
    df = cargar_dayc()
    return df.to_dict(orient="records")

@app.get("/api/pet")
def obtener_pet():
    df = cargar_pet()
    return df.to_dict(orient="records")

@app.get("/api/seni")
def obtener_seni():
    df = cargar_seni()
    return df.to_dict(orient="records")

@app.get("/api/event_s")
def obtener_event_s():
    df = cargar_event_s()
    return df.to_dict(orient="records")

@app.get("/api/event_c")
def obtener_event_c():
    df = cargar_event_c()
    return df.to_dict(orient="records")

@app.get("/api/shop")
def obtener_shop():
    df = cargar_shop()
    return df.to_dict(orient="records")

@app.get("/api/super")
def obtener_super():
    df = cargar_super()
    return df.to_dict(orient="records")

@app.get("/api/auto")
def obtener_auto():
    df = cargar_auto()
    return df.to_dict(orient="records")

@app.get("/api/gas")
def obtener_gas():
    df = cargar_gas()
    return df.to_dict(orient="records")

@app.get("/api/gym")
def obtener_gym():
    df = cargar_gym()
    return df.to_dict(orient="records")

@app.get("/api/venue")
def obtener_venue():
    df = cargar_venue()
    return df.to_dict(orient="records")

@app.get("/api/restaurant")
def obtener_restaurant():
    df = cargar_restaurant()
    return df.to_dict(orient="records")

@app.get("/api/hotel")
def obtener_hotel():
    df = cargar_hotel()
    return df.to_dict(orient="records")

@app.get("/api/religious_building")
def obtener_religious_building():
    df = cargar_religious_building()
    return df.to_dict(orient="records")

@app.get("/api/park")
def obtener_park():
    df = cargar_park()
    return df.to_dict(orient="records")