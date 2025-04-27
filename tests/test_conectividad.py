import requests

def test_conectividad_basica():
    url = "http://localhost:8080/api/greenlake-eval/test"
    response = requests.get(url)

    # Verificamos solo que responde correctamente
    assert response.status_code == 200

    # Imprimimos el JSON de respuesta
    print(response.json())

test_conectividad_basica()