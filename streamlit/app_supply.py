import streamlit as st
import pandas as pd
import requests

st.title("Visualización de lugares de compra")

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
url_shop = "http://localhost:8080/api/shop"
url_gas = "http://localhost:8080/api/gas_station"
url_super = "http://localhost:8080/api/supermarket"
url_auto = "http://localhost:8080/api/auto_service"
url_cities = "http://localhost:8080/api/cities"


# Cargar los DataFrames
df_shop = cargar_datos(url_shop)
df_gas = cargar_datos(url_gas)
df_super = cargar_datos(url_super)
df_auto = cargar_datos(url_auto)
df_C = cargar_datos(url_cities)

# Renombramos columna para hacer el merge más fácil en df_C
if not df_C.empty:
    df_C = df_C.rename(columns={'name': 'city_name'})

# --- Merge con city_name ---
# Para df_shop
if not df_shop.empty:
    df_shop = df_shop.merge(
        df_C[['id', 'city_name']],        
        left_on='city_id',                
        right_on='id',                    
        how='left'                        
    )

# Para df_gas
if not df_gas.empty:
    df_gas = df_gas.merge(
        df_C[['id', 'city_name']],        
        left_on='city_id',                
        right_on='id',                    
        how='left'                        
    )

# Para df_super
if not df_super.empty:
    df_super = df_super.merge(
        df_C[['id', 'city_name']],        
        left_on='city_id',                
        right_on='id',                    
        how='left'                        
    )

# Para df_auto
if not df_auto.empty:
    df_auto = df_auto.merge(
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
show_table = st.radio('¿Qué quieres hacer?', [ 'Ir a comprar comida',
                                               'Repostar',
                                               'Ver las tablas de datos disponibles',
                                               "Ver información de sostenibilidad"])

# # Si el botón es presionado, mostramos la tabla

if show_table=='Ver las tablas de datos disponibles':
    st.write("Aquí está la tabla de datos de tiendas:")
    # st.write(df_shop.columns)
    st.dataframe(df_shop)
    st.write("Aquí está la tabla de datos de supermercados:")
    #st.write(df_super.columns)
    st.dataframe(df_super)
    st.write("Aquí está la tabla de datos de gasolineras:")
    # st.write(df_gas.columns)
    st.dataframe(df_gas)
    st.write("Aquí está la tabla de datos de estaciones de autoservicio:")
    # st.write(df_auto.columns)
    st.dataframe(df_auto)

elif show_table == 'Ir a comprar comida':
    df_comp = pd.DataFrame()
    # Filtrar df_gas solo si has_convenience_store es True
    df_gas_filtered = df_gas[df_gas['has_convenience_store'] == True]
    
    # Segundo radio para escoger entre eco, auto servicio o gran superficie
    product_option = st.radio("Selecciona el tipo de productos", ("Eco", "Auto servicio", "Gran superficie"))
    
    if product_option == "Eco":
        # Filtrar según los productos eco, auto servicio y gran superficie
        df_shop_filtered = df_shop[df_shop['eco_friendly_products'] == True]
        df_super_filtered = df_super[df_super['local_organic_products'] == True]
        df_auto_filtered = df_auto[df_auto['eco_friendly_services'] == True]
        
        # Combinar en df_comp
        df_comp = pd.concat([df_shop_filtered, df_super_filtered, df_auto_filtered])

    elif product_option == "Auto servicio":
        # Solo df_auto
        df_auto_filtered = df_auto
        df_comp = df_auto_filtered

    elif product_option == "Gran superficie":
        # Solo df_super
        df_super_filtered = df_super
        df_comp = df_super_filtered

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
    st.success("¡Le deseamos una buena compra!")


elif show_table == "Repostar":
    df_comp = pd.DataFrame()    
    # Radio para escoger entre gasolina o eléctrico
    fuel_option = st.radio("Selecciona el tipo de repostaje", ("Gasolina", "Eléctrico"))
    
    if fuel_option == "Gasolina":
        # Solo df_gas
        df_gas_filtered = df_gas
        df_comp = df_gas_filtered

    elif fuel_option == "Eléctrico":
        # Filtrar df_gas y df_auto con electric_vehicle_charging == True
        df_gas_filtered = df_gas[df_gas['electric_vehicle_charging'] == True]
        df_auto_filtered = df_auto[df_auto['electric_vehicle_charging'] == True]
        
        # Combinar en df_comp
        df_comp = pd.concat([df_gas_filtered, df_auto_filtered])

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
    df_shop[common_columns],
    df_super[common_columns],
    df_gas[common_columns],
    df_auto[common_columns]
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
