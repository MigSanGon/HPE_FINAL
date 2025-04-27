import streamlit as st
import pandas as pd
import requests

def app(change_page_func):  # 👈 El cambio_page_func ya está como parámetro
    # Inicializar página actual
    if "page" not in st.session_state:
        st.session_state.page = "descan"
    st.title("Visualización de infraestructuras general")

    # Función para cargar datos
    @st.cache_data
    def cargar_datos(url):
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"No se pudieron cargar los datos de la API: {url}")
            return pd.DataFrame()

    # Cargar ciudades
    url_cities = "http://localhost:8080/api/cities"
    df_C = cargar_datos(url_cities)

    if not df_C.empty:
        df_C = df_C.rename(columns={'name': 'city_name'})

    def cargar_y_combinar_datos(tipo_edificios, df_C):
        for tipo in tipo_edificios:
            url = f"http://localhost:8080/api/{tipo.lower().replace(' ', '_')}"
            df = cargar_datos(url)

            if not df.empty:
                df = df.merge(
                    df_C[['id', 'city_name']],
                    left_on='city_id',
                    right_on='id',
                    how='left'
                )
            else:
                st.write(f"No se encontraron datos para {tipo}.")
            return df

    # UI de selección
    col1, col2 = st.columns(2)

    with col1:
        show_tables = st.button('Ver las tablas de datos disponibles', key="button_tablas")
    with col2:
        show_sustainability = st.button('Ver información de sostenibilidad', key="button_sostenibilidad")

    tipos_edificios = [
        'Shop', 'Hospital', 'Religious Building', 'Pharmacy', 'Venue',
        'Healthcare Clinic', 'Gas Station', 'School', 'Daycare', 'Park', 'Restaurant',
        'Office Building', 'Supermarket', 'Bank', 'Hotel', 'Transportation Hub', 'Gym',
        'Auto Service', 'Laundromat', 'Salon', 'Pet Services', 'Government Building',
        'Senior Living', 'Fabric'
    ]

    if show_tables:
        seleccionados = st.multiselect("Selecciona los tipos de edificios", tipos_edificios, key="multiselect_tablas")
        for i in seleccionados:
            df = cargar_y_combinar_datos([i], df_C)
            st.write(f"Aquí está la tabla de datos de {i}:")
            st.dataframe(df)

    elif show_sustainability:
        seleccionados = st.multiselect("Selecciona los tipos de edificios", tipos_edificios, key="multiselect_sostenibilidad")
        for i in seleccionados:
            df = cargar_y_combinar_datos([i], df_C)

            cities = df['city_name'].dropna().unique()
            selected_city = st.selectbox("Selecciona la ciudad:", sorted(cities), key=f"city_select_{i}")

            filtered_df = df[df['city_name'] == selected_city]

            st.dataframe(filtered_df[['name', 'type', 'subtype', 'city_name']])

            st.markdown("---")

            selected_metrics = st.multiselect(
                "Selecciona las métricas que quieres comparar:",
                ['green_score', 'carbon_footprint_kg_per_year', 'energy_efficiency_score',
                 'water_efficiency_score', 'waste_management_score', 'renewable_energy_percentage'],
                default=['green_score', 'energy_efficiency_score'],
                key=f"metrics_select_{i}"
            )

            if selected_metrics:
                st.subheader("Gráfica comparativa de las infraestructuras")
                chart_data = filtered_df[['name'] + selected_metrics].set_index('name')
                st.bar_chart(chart_data)

    # st.header('Aquí hay más utilidades para los ciudadanos')
    

    # Función para cambiar de página
    def change_page(page_name):
        st.session_state.page = page_name
    # Botones de navegación usando el cambio_page_func que te pasan
    
        if st.button(" 🩺 Salud 💊 ", key="button_salud"):
            change_page_func("salud")
            from app_med import app
            app(change_page)

        if st.button("👶 Asistencia 🐶", key="button_asistencia"):
            change_page_func("asis")
            from app_asist import app
            app(change_page)

        if st.button("🛒 Compras 🚐", key="button_compras"):
            change_page_func("compra")
            from app_supply import app
            app(change_page)

    # elif st.session_state.page == "salud":
    #     from app_med import app
    #     app(change_page)

    # elif st.session_state.page == "asis":
    #     from app_asist import app
    #     app(change_page)

    # elif st.session_state.page == "compra":
    #     from app_supply import app
    #     app(change_page)

    


    # Botón para volver al inicio
    st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)
    if st.button("🏠 Volver al Inicio", key="button_inicio"):
        change_page_func("home")
