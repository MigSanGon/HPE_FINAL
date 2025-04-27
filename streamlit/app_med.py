import streamlit as st
import pandas as pd
import requests

st.title("Visualización de centros sanitarios")

# Llamada a la API
url_H = "http://localhost:8080/api/med"
response = requests.get(url_H)

if response.status_code == 200:
    data = response.json()
    df_H = pd.DataFrame(data)
    
else:
    st.error("No se pudieron cargar los datos de la API.")

url_HC = "http://localhost:8080/api/clin"
response = requests.get(url_HC)

if response.status_code == 200:
    data = response.json()
    df_HC = pd.DataFrame(data)
    
else:
    st.error("No se pudieron cargar los datos de la API.")

url_Ph = "http://localhost:8080/api/phar"
response = requests.get(url_Ph)

if response.status_code == 200:
    data = response.json()
    df_Ph = pd.DataFrame(data)
    
else:
    st.error("No se pudieron cargar los datos de la API.")

url_C = "http://localhost:8080/api/cities"
response = requests.get(url_C)

if response.status_code == 200:
    data = response.json()
    df_C = pd.DataFrame(data)
    df_C =df_C.rename(columns={'name': 'city_name'})
    #st.dataframe(df_C)
else:
    st.error("No se pudieron cargar los datos de la API.")


# Recorremos cada DataFrame y realizamos el merge correctamente
for i, DF in enumerate([df_H, df_HC, df_Ph]):
    # Realizamos el merge y reasignamos el resultado a DF
    if i == 0:
        df_H = DF.merge(
            df_C[['id', 'city_name']],           # Seleccionamos id y city_name
            left_on='city_id',                   # Columna de df_H
            right_on='id',                       # Columna de df_C
            how='left'                           # Mantener todas las filas de df_H
        )
    elif i == 1:
        df_HC = DF.merge(
            df_C[['id', 'city_name']],           # Seleccionamos id y city_name
            left_on='city_id',                   # Columna de df_HC
            right_on='id',                       # Columna de df_C
            how='left'                           # Mantener todas las filas de df_HC
        )
    elif i == 2:
        df_Ph = DF.merge(
            df_C[['id', 'city_name']],           # Seleccionamos id y city_name
            left_on='city_id',                   # Columna de df_Ph
            right_on='id',                       # Columna de df_C
            how='left'                           # Mantener todas las filas de df_Ph
        )





#HASTA AQUÍ LA CARGA DE DATOS: AHORA TOCA JUGAR


# Función para filtrar los DataFrames
def filter_df_by_city(df, city_name):
    return df[df['city_name'] == city_name]

# Mostrar una pregunta para saber si necesita asistencia médica
show_table = st.radio('¿Qué quieres hacer?', ['Asistencia médica',
                                               'Ver las tablas de información disponible',
                                               "Ver información de sostenibilidad"])

# Si el botón es presionado, mostramos la tabla

if show_table=='Ver las tablas de información disponible':
    st.write("Aquí está la tabla de datos de hospitales:")
    st.write(df_H.columns)
    st.dataframe(df_H)
    st.write("Aquí está la tabla de datos de clínicas:")
    st.write(df_HC.columns)
    st.dataframe(df_HC)
    st.write("Aquí está la tabla de datos de farmacias:")
    st.write(df_Ph.columns)
    st.dataframe(df_Ph)

elif show_table=="Ver información de sostenibilidad":
    st.write("¿Qué clase de información quiere?")
    common_columns = [
    'infra_id', 'name', 'type', 'subtype', 'city_name', 'opening_date',
    'green_score', 'carbon_footprint_kg_per_year', 'energy_efficiency_score',
    'water_efficiency_score', 'waste_management_score',
    'renewable_energy_percentage', 'green_certification', 'location'
]

    # Concatenamos todos
    df_all = pd.concat([
    df_H[common_columns],
    df_HC[common_columns],
    df_Ph[common_columns]
    ], axis=0)

    # Filtro por ciudad
    cities = df_all['city_name'].dropna().unique()
    selected_city = st.selectbox("Selecciona la ciudad:", sorted(cities))

    # Filtrar según ciudad
    filtered_df = df_all[df_all['city_name'] == selected_city]

    # Mostrar tabla
    st.dataframe(filtered_df[['name', 'type', 'subtype', 'city_name']])

    # Divider
    st.markdown("---")

    # Selección de métricas para comparar
    selected_metrics = st.multiselect(
        "Selecciona las métricas que quieres comparar:",
        ['green_score', 'carbon_footprint_kg_per_year', 'energy_efficiency_score',
        'water_efficiency_score', 'waste_management_score', 'renewable_energy_percentage'],
        default=['green_score', 'energy_efficiency_score']
    )

    if selected_metrics:
        st.subheader("Gráfica comparativa de las infraestructuras")
        
        chart_data = filtered_df[['name'] + selected_metrics].set_index('name')
        st.bar_chart(chart_data)
else:
        
    # Preguntar si la asistencia es urgente
    is_urgent = st.radio("¿Es urgente?", ['Sí', 'No'])
    
    # Filtrar según la urgencia
    if is_urgent == 'Sí':
        # Eliminar df_Ph y filtrar df_HC para que solo contenga 'Urgent Care'
        filtered_df_HC = df_HC[df_HC['subtype'] == 'Urgent Care']
        available_datasets = pd.concat([filtered_df_HC, df_H])
        st.write("Está buscando asistencia urgente. Solo se muestran opciones de clínicas con urgencias u hospitales.")
    else:
        # Eliminar df_H (hospitales) si no es urgente
        available_datasets = pd.concat([df_HC, df_Ph])
        st.write("Está buscando asistencia no urgente. Se muestran opciones de clínicas y farmacias.")

    # Preguntar por la ciudad
    city_name = st.selectbox("Selecciona la ciudad:", options=[''] + list(df_H['city_name'].unique()))
    
    if city_name:
        # Filtrar los DataFrames por la ciudad seleccionada
        filtered_data = filter_df_by_city(available_datasets, city_name)
        
        columns_to_remove = ['infra_id', "id_x", "id_y",'city_id',  'city_name', 'opening_date',
        'green_score', 'carbon_footprint_kg_per_year', 'energy_efficiency_score',
        'water_efficiency_score', 'waste_management_score',
        'renewable_energy_percentage', 'green_certification', 'location']
        selected_columns_df = filtered_data.drop(columns_to_remove,axis=1)

        # Mostrar el DataFrame filtrado en Streamlit
        st.dataframe(selected_columns_df)
    

