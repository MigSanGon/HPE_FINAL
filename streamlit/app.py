import streamlit as st
import pandas as pd
import requests

st.title("Visualización de Cities")

# Llamada a la API
url = "http://localhost:8000/api/cities"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    st.dataframe(df)
else:
    st.error("No se pudieron cargar los datos de la API.")
