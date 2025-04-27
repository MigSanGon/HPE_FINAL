import streamlit as st
import pandas as pd
import requests

st.title("Visualización de lugares de ocio")

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
# --- Cargar datos desde la API ---
url_venue = "http://localhost:8080/api/venue"
url_gym = "http://localhost:8080/api/gym"
url_park = "http://localhost:8080/api/park"
url_hotel = "http://localhost:8080/api/hotel"
url_religious_building = "http://localhost:8080/api/religious_building"
url_restaurant = "http://localhost:8080/api/restaurant"
url_cities = "http://localhost:8080/api/cities"

# Cargar los DataFrames
df_venue = cargar_datos(url_venue)
df_gym = cargar_datos(url_gym)
df_park = cargar_datos(url_park)
df_hotel = cargar_datos(url_hotel)
df_religious_building = cargar_datos(url_religious_building)
df_restaurant = cargar_datos(url_restaurant)
df_C = cargar_datos(url_cities)

# Renombramos columna para hacer el merge más fácil en df_C
if not df_C.empty:
    df_C = df_C.rename(columns={'name': 'city_name'})

# --- Merge con city_name ---
# Para df_venue
if not df_venue.empty:
    df_venue = df_venue.merge(
        df_C[['id', 'city_name']],        
        left_on='city_id',                
        right_on='id',                    
        how='left'                        
    )

# Para df_gym
if not df_gym.empty:
    df_gym = df_gym.merge(
        df_C[['id', 'city_name']],        
        left_on='city_id',                
        right_on='id',                    
        how='left'                        
    )

# Para df_park
if not df_park.empty:
    df_park = df_park.merge(
        df_C[['id', 'city_name']],        
        left_on='city_id',                
        right_on='id',                    
        how='left'                        
    )

# Para df_hotel
if not df_hotel.empty:
    df_hotel = df_hotel.merge(
        df_C[['id', 'city_name']],        
        left_on='city_id',                
        right_on='id',                    
        how='left'                        
    )

# Para df_religious_building
if not df_religious_building.empty:
    df_religious_building = df_religious_building.merge(
        df_C[['id', 'city_name']],        
        left_on='city_id',                
        right_on='id',                    
        how='left'                        
    )

# Para df_restaurant
if not df_restaurant.empty:
    df_restaurant = df_restaurant.merge(
        df_C[['id', 'city_name']],        
        left_on='city_id',                
        right_on='id',                    
        how='left'                        
    )





#HASTA AQUÍ LA CARGA DE DATOS: AHORA TOCA JUGAR

# # Función para filtrar los DataFrames
# def filter_df_by_city(df, city_name):
#     return df[df['city_name'] == city_name]

# # Mostrar una pregunta para saber si necesita asistencia médica
show_table = st.radio('¿Qué quieres hacer?', [ 'Descansar',
                                               'Disfrutar',
                                               'Pasear o socializar',
                                               'Comer',
                                               'Ver las tablas de datos disponibles',
                                               "Ver información de sostenibilidad"])

# # Si el botón es presionado, mostramos la tabla

if show_table=='Ver las tablas de datos disponibles':
    st.write("Aquí está la tabla de datos de gimnasios:")
    st.write(df_gym.columns)
    st.dataframe(df_gym)
    st.write("Aquí está la tabla de datos de parques:")
    st.write(df_park.columns)
    st.dataframe(df_park)
    st.write("Aquí está la tabla de datos de restaurantes:")
    st.write(df_restaurant.columns)
    st.dataframe(df_restaurant)
    st.write("Aquí está la tabla de datos de restaurantes:")
    st.write(df_venue.columns)
    st.dataframe(df_venue)
    # st.write("Aquí está la tabla de datos de hoteles:")
    # st.write(df_hotel.columns)
    # st.dataframe(df_hotel)
    # st.write("Aquí está la tabla de datos de edificios religiosos:")
    # st.write(df_religious_building.columns)
    # st.dataframe(df_religious_building)

elif show_table == 'Descansar':
    df_comp = pd.DataFrame()
    
    cities = df_comp['city_name'].dropna().unique()
    selected_city = st.selectbox("Selecciona la ciudad:", sorted(cities))
    resultados =  df_comp[df_comp['city_name'] == selected_city]
    st.subheader("Opciones disponibles")
    
    columns_to_remove = ['infra_id', "id_x", "id_y",'city_id',  'city_name', 'opening_date',
        'green_score', 'carbon_footprint_kg_per_year', 'energy_efficiency_score',
        'water_efficiency_score', 'waste_management_score',
        'renewable_energy_percentage', 'green_certification', 'location']
    selected_columns_df = resultados.drop(columns_to_remove,axis=1)

    # Mostrar el DataFrame filtrado en Streamlit
    st.dataframe(selected_columns_df)
    st.success("¡Le deseamos una buena compra!")


elif show_table == "Repostar":
    df_comp = pd.DataFrame()    


    cities = df_comp['city_name'].dropna().unique()
    selected_city = st.selectbox("Selecciona la ciudad:", sorted(cities))
    # Filtrar según tipo
    
    resultados =  df_comp[df_comp['city_name'] == selected_city]
    

    st.subheader("Opciones disponibles")
    columns_to_remove = ['infra_id', "id_x", "id_y",'city_id',  'city_name', 'opening_date',
    'green_score', 'carbon_footprint_kg_per_year', 'energy_efficiency_score',
    'water_efficiency_score', 'waste_management_score',
    'renewable_energy_percentage', 'green_certification', 'location']
    selected_columns_df = resultados.drop(columns_to_remove,axis=1)

    # Mostrar el DataFrame filtrado en Streamlit
    st.dataframe(selected_columns_df)

    st.success("¡Le deseamos un buen viaje!")

elif show_table== "Ver información de sostenibilidad":
    
    common_columns = [
    'infra_id', 'name', 'type', 'subtype', 'city_name', 'opening_date',
    'green_score', 'carbon_footprint_kg_per_year', 'energy_efficiency_score',
    'water_efficiency_score', 'waste_management_score',
    'renewable_energy_percentage', 'green_certification', 'location'
]

    # Concatenamos todos
    df_all = pd.concat([
    df_gym[common_columns],
    df_park[common_columns],
    df_religious_building[common_columns],
    df_hotel[common_columns],
    df_restaurant[common_columns],
    df_venue[common_columns]
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
