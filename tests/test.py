import requests

def test_conectividad_basica():
    url = "http://localhost:8080/api/greenlake-eval/test"
    response = requests.get(url)

    # Verificamos solo que responde correctamente
    assert response.status_code == 200

    # Imprimimos el JSON de respuesta
    print(response.json())

test_conectividad_basica()


def test_hospitals_nearby():
    url = "http://localhost:8080/api/greenlake-eval/hospitals/nearby"
    params = {
        "lat": 79.8965515,
        "lon": -48.0003246,
        "radius": 1000
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("✅ API respondió correctamente")
        print(response.json())
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

# Ejecutar test
test_hospitals_nearby()
