import streamlit as st
import pandas as pd
import requests

st.title("Visualización de infraestructuras general")

# Llamada a la API para cargar datos
def cargar_datos(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        st.error(f"No se pudieron cargar los datos de la API: {url}")
        return pd.DataFrame()

# --- Cargar datos desde la API ---


url_cities = "http://localhost:8080/api/cities"

# Cargar los DataFrames
# df_venue = cargar_datos(url_venue)

df_C = cargar_datos(url_cities)

# Renombramos columna para hacer el merge más fácil en df_C
if not df_C.empty:
    df_C = df_C.rename(columns={'name': 'city_name'})


# Función para cargar los datos desde una URL
def cargar_datos(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        return pd.DataFrame()

# Función principal que maneja la lógica de cargar y combinar los datos
def cargar_y_combinar_datos(tipo_edificios, df_C):
    for tipo in tipo_edificios:
        # URL dinámica para cada tipo de infraestructura
        url = f"http://localhost:8080/api/{tipo.lower().replace(' ', '_')}"
        df = cargar_datos(url)
        
        # Si hay datos, realizar el merge
        if not df.empty:
            df = df.merge(
                df_C[['id', 'city_name']],        
                left_on='city_id',                
                right_on='id',                    
                how='left'                        
            )
            st.write(f"Aquí está la tabla de datos de {tipo}:")
            
            st.dataframe(df)
        else:
            st.write(f"No se encontraron datos para {tipo}.")

# Streamlit - Interfaz de usuario



#HASTA AQUÍ LA CARGA DE DATOS: AHORA TOCA JUGAR

# # Función para filtrar los DataFrames
# def filter_df_by_city(df, city_name):
#     return df[df['city_name'] == city_name]

# # Mostrar una pregunta para saber si necesita asistencia médica
show_table = st.radio('¿Qué quieres hacer?', [ 'Ver las tablas de datos disponibles',
                                               "Ver información de sostenibilidad"])

# # Si el botón es presionado, mostramos la tabla
tipos_edificios = [
        'Shop', 'Hospital', 'Religious Building', 'Pharmacy', 'Venue',
        'Healthcare Clinic', 'Gas Station', 'School', 'Daycare', 'Park', 'Restaurant',
        'Office Building', 'Supermarket', 'Bank', 'Hotel', 'Transportation Hub', 'Gym',
        'Auto Service', 'Laundromat', 'Salon', 'Pet Services', 'Government Building',
        'Senior Living', 'Fabric'
    ]
if show_table=='Ver las tablas de datos disponibles':
    
    
    # Selector múltiple para que el usuario elija los tipos de edificios
    seleccionados = st.multiselect("Selecciona los tipos de edificios", tipos_edificios)
    for i in seleccionados:
        cargar_y_combinar_datos([i], df_C)

elif show_table== "Ver información de sostenibilidad":
    
    common_columns = [
    'infra_id', 'name', 'type', 'subtype', 'city_name', 'opening_date',
    'green_score', 'carbon_footprint_kg_per_year', 'energy_efficiency_score',
    'water_efficiency_score', 'waste_management_score',
    'renewable_energy_percentage', 'green_certification', 'location'
]

    

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
