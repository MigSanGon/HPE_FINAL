import streamlit as st
import pandas as pd
import requests

def app(change_page_func):
    st.title("Visualización de centros asistencia")

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
    url_pet = "http://localhost:8080/api/pet_services"
    url_dayc = "http://localhost:8080/api/daycare"
    url_seni = "http://localhost:8080/api/senior_living"
    url_event_c = "http://localhost:8080/api/event_c"
    url_event_s = "http://localhost:8080/api/event_s"
    url_cities = "http://localhost:8080/api/cities"

    df_pet = cargar_datos(url_pet)
    df_dayc = cargar_datos(url_dayc)
    df_senior = cargar_datos(url_seni)
    df_event_c = cargar_datos(url_event_s)
    df_event_s = cargar_datos(url_event_c)
    df_C = cargar_datos(url_cities)

    # Renombramos columna para hacer el merge más fácil
    if not df_C.empty:
        df_C = df_C.rename(columns={'name': 'city_name'})

    # --- Merge con city_name ---
    for i, DF in enumerate([df_pet, df_dayc, df_senior, df_event_s, df_event_c]):
        if i == 0:
            df_pet = DF.merge(
                df_C[['id', 'city_name']],        
                left_on='city_id',                
                right_on='id',                    
                how='left'                        
            )
        elif i == 1:
            df_dayc = DF.merge(
                df_C[['id', 'city_name']],        
                left_on='city_id',                
                right_on='id',                    
                how='left'                        
            )
        elif i == 2:
            df_senior = DF.merge(
                df_C[['id', 'city_name']],        
                left_on='city_id',                
                right_on='id',                    
                how='left'                        
            )
        elif i == 3:
            df_event_s = DF.merge(
                df_C[['id', 'city_name']],        
                left_on='city_id',                
                right_on='id',                    
                how='left'                        
            )
        elif i == 4:
            df_event_c = DF.merge(
                df_C[['id', 'city_name']],        
                left_on='city_id',                
                right_on='id',                    
                how='left'                        
            )


    # # Mostrar una pregunta para saber si necesita asistencia médica
    show_table_a = st.radio('¿Qué requiere?', ['Asistencia para niños',
                                                'Asistencia para tercera edad',
                                                'Asistencia para mascotas',
                                                'Ver las tablas de datos disponibles',
                                                "Ver información de sostenibilidad"],key='a')

    # # Si el botón es presionado, mostramos la tabla

    if show_table_a=='Ver las tablas de datos disponibles':
        st.write("Aquí está la tabla de datos de veterinarios:")
        # st.write(df_pet.columns)
        st.dataframe(df_pet)
        st.write("Aquí está la tabla de datos de centros de mayores:")
        # st.write(df_senior.columns)
        st.dataframe(df_senior)
        st.write("Aquí está la tabla de datos de guarderías:")
        # st.write(df_dayc.columns)
        st.dataframe(df_dayc)

    elif show_table_a == 'Asistencia para niños':
        
            edad = st.slider('¿Qué edad tiene el niño?', 0, 12, 3)

            if edad <= 2:
                tipo = "Infant Care"
            elif 3 <= edad <= 5:
                tipo = "Preschool"
            elif 6 <= edad <= 10:
                tipo = "After School"
            elif edad <= 12:
                tipo = "Family Daycare"
        

            # Filtramos el dataframe
            # Filtro por ciudad
            cities = df_dayc['city_name'].dropna().unique()
            selected_city = st.selectbox("Selecciona la ciudad:", sorted(cities))

            # Filtrar según tipo
            filtered_df = df_dayc[df_dayc['city_name'] == selected_city]
            resultados = filtered_df[filtered_df['subtype'] == tipo]

            st.subheader(f"Opciones para: {tipo}")
            columns_to_show = ["name",  "subtype", "age_range", "eco_friendly_toys", "outdoor_learning_space"]
            selected_columns_df = resultados[columns_to_show]

            # Mostrar el DataFrame filtrado en Streamlit
            st.dataframe(selected_columns_df)
            if filtered_df[filtered_df['subtype'] == tipo].empty:  
                pass
            else:
                montesori=st.radio('¿Desea una alternativa Montessori?',['Sí', 'No'])
                if montesori == 'Sí':
                    resultados = filtered_df[filtered_df['subtype'] == "Montessori"]
                    st.subheader(f"Opciones para: Montessori")
                    columns_to_show = ["name",  "subtype", "age_range", "eco_friendly_toys", "outdoor_learning_space"]
                    selected_columns_df = resultados[columns_to_show]

                    # Mostrar el DataFrame filtrado en Streamlit
                    st.dataframe(selected_columns_df)

            st.success("¡Le deseamos una feliz estancia al niño!")
            
            eve_c=st.radio("Si desea recuperar el tiempo perdido: ¿quiere una recomendación de eventos a los que pueda acudir con su familia?",['Sí','No'])
            if eve_c=='Sí':
                filtered_ = df_event_c[df_event_c['city_name'] == selected_city]
                columns_to_show = ["name",  "description", "start_date", "end_date","satisfaction_score"]
                selected_columns_ = filtered_[columns_to_show]

                # Mostrar el DataFrame filtrado en Streamlit
                st.dataframe(selected_columns_)






    elif show_table_a == "Asistencia para tercera edad":
            asistencia = st.radio(
                "¿Qué tipo de asistencia necesita?",
                ("Asistencia en su casa", "Nuevo hogar")
            )

            if asistencia == "Asistencia en su casa":
                tipos = ["Assisted Living", "Senior Apartments"]
            else:
                tipos = ["Nursing Home", "Retirement Home", "Memory Care"]

            # Filtro por ciudad
            cities = df_senior['city_name'].dropna().unique()
            selected_city = st.selectbox("Selecciona la ciudad:", sorted(cities))

            # Filtrar según tipo
            filtered_df = df_senior[df_senior['city_name'] == selected_city]
            resultados = filtered_df[filtered_df['subtype'].isin(tipos)]

            st.subheader("Opciones disponibles")
            columns_to_show = ["name", "subtype", "staff_count", "energy_efficient_heating", "water_conservation_systems"]
            selected_columns_df = resultados[columns_to_show]

            # Mostrar el DataFrame filtrado en Streamlit
            st.dataframe(selected_columns_df)

            st.success("¡Le deseamos que siga muchos años acompañado de su familia!")

            eve_s=st.radio("Si desea recuperar el tiempo perdido: ¿quiere una recomendación de eventos a los que pueda acudir con su familia?",['Sí','No'])
            if eve_s=='Sí':
                filtered_ = df_event_s[df_event_s['city_name'] == selected_city]
                columns_to_show = ["name",  "description", "start_date", "end_date","satisfaction_score"]
                selected_columns_ = filtered_[columns_to_show]

                # Mostrar el DataFrame filtrado en Streamlit
                st.dataframe(selected_columns_)

    elif show_table_a == 'Asistencia para mascotas':
            motivo = st.radio(
                "¿Motivo de la asistencia?",
                ("Veterinario", "No puedo hacerme cargo")
            )

            if motivo == "Veterinario":
                tipo = "Veterinary Clinic"
            else:
                tipo = "Pet Adoption"

            cities = df_pet['city_name'].dropna().unique()
            selected_city = st.selectbox("Selecciona la ciudad:", sorted(cities))

            # Filtrar según tipo
            filtered_df = df_pet[df_pet['city_name'] == selected_city]
            resultados = filtered_df[filtered_df['subtype'] == tipo]

            st.subheader(f"Opciones para: {tipo}")
            st.subheader("Opciones disponibles")
            columns_to_show = ["name", "sustainable_waste_disposal", "energy_efficient_equipment", "eco_friendly_products"]
            selected_columns_df = resultados[columns_to_show]

            # Mostrar el DataFrame filtrado en Streamlit
            st.dataframe(selected_columns_df)


            st.success("¡Esperamos que su mascota esté en las mejores manos!")
    elif show_table_a== "Ver información de sostenibilidad":
        
        common_columns = [
        'infra_id', 'name', 'type', 'subtype', 'city_name', 'opening_date',
        'green_score', 'carbon_footprint_kg_per_year', 'energy_efficiency_score',
        'water_efficiency_score', 'waste_management_score',
        'renewable_energy_percentage', 'green_certification', 'location'
    ]

        # Concatenamos todos
        df_all = pd.concat([
        df_pet[common_columns],
        df_senior[common_columns],
        df_dayc[common_columns]
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


    #Botón para volver al inicio
    st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)
    if st.button("🏠 Volver al Inicio"):
        change_page_func("home")
