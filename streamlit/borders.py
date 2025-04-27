import streamlit as st
import pandas as pd
import requests
from shapely import wkt
from shapely.geometry import Polygon, MultiPolygon
import pydeck as pdk

# Función para cargar estados

def convertir_wkt_a_coordenadas(wkt_string):
    geom = wkt.loads(wkt_string)
    if isinstance(geom, Polygon):
        # Si es un solo polígono
        return [list(geom.exterior.coords)]
    elif isinstance(geom, MultiPolygon):
        # Si es multipolígono: lista de polígonos
        return [list(p.exterior.coords) for p in geom.geoms]
    else:
        return None

def convertir_parcel_vertices(vertices_string):
    points = vertices_string.strip().split(';')
    coords = []
    for point in points:
        if point:  # Evitar vacíos
            lat, lon = map(float, point.split(','))
            coords.append([lon, lat])  
    return [coords]  # Devolver lista de listas para PolygonLayer


def calcular_centro(coordinates):
    if coordinates and isinstance(coordinates, list):
        return Polygon(coordinates[0]).centroid
    else:
        return None
    
@st.cache_data
def cargar_estados():
    url = "http://localhost:8080/api/state_borders"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        df['coordinates'] = df['vertices'].apply(convertir_wkt_a_coordenadas)
        return df
    else:
        st.error("No se pudieron cargar los datos de la API.")

@st.cache_data
def cargar_ciudades():
    url = f"http://localhost:8080/api/city_borders"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        df['coordinates'] = df['vertices'].apply(convertir_wkt_a_coordenadas)
        return df
    else:
        st.error("No se pudieron cargar los datos de la API.")

@st.cache_data
def cargar_parcels():
    url = f"http://localhost:8080/api/parcels"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        df['coordinates'] = df['vertices'].apply(convertir_parcel_vertices)
        return df
    else:
        st.error("No se pudieron cargar los datos de la API.")
    
st.title("Mapas interactivos: Países y Ciudades ")

opcion = st.radio(
    "¿Qué quieres hacer?",
    ("Ver tablas de datos", "Ver visualizaciones interactivas")
)

if opcion == "Ver tablas de datos":
    st.header("Tablas de Datos")

    df_states = cargar_estados()
    df_cities = cargar_ciudades()  
    df_parcels = cargar_parcels()  

    if st.checkbox("Mostrar tabla de países"):
        st.dataframe(df_states)

    if st.checkbox("Mostrar tabla de ciudades"):
        df_cities = df_cities.merge(
                df_states[['state_id', 'state_name']],
                on='state_id',
                how='left'
            )
        df_cities = df_cities.drop(columns=['state_id'])
        st.dataframe(df_cities)

    if st.checkbox("Mostrar tabla de parcelas"):
        df_parcels = df_parcels.merge(
            df_cities[['city_id', 'city_name']],
            on='city_id',
            how='left'
        )
        df_parcels = df_parcels.drop(columns=['city_id'])
        st.dataframe(df_parcels)

elif opcion == "Ver visualizaciones interactivas":

    # Cargar estados
    df_states = cargar_estados()
    df_states['area_km2'] = df_states['area_km2'].round(1)

    if not df_states.empty:
    
        # --- 1. MOSTRAR TODOS LOS PAÍSES ---
        states_layer = pdk.Layer(
            "PolygonLayer",
            data=df_states,
            get_polygon="coordinates",
            get_fill_color="[200, 30, 0, 100]",
            get_line_color="[0, 0, 0, 150]",
            line_width_min_pixels=1,
            pickable=True,
            extruded=False,
        )

        tooltip_states = {
            "html": "<b>País:</b> {state_name}<br/><b>Área:</b> {area_km2} km²",
            "style": {"backgroundColor": "black", "color": "white"}
        }

        st.subheader("Todos los países")
        if st.checkbox("Mostrar todos los países"):
            st.dataframe(df_states)

        # Vista inicial centrada en el mundo
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=72,  # Ajusta el centro inicial
                longitude=-42,
                zoom=1.5,
                pitch=0,
            ),
            layers=[states_layer],
            tooltip=tooltip_states
        ))

        st.markdown("---")

        # --- 2. SELECCIONAR UN PAÍS ---
        selected_state = st.selectbox("Selecciona un país para explorar:", df_states['state_name'].unique())

        if selected_state:
            state_row = df_states[df_states['state_name'] == selected_state].iloc[0]
            state_id = state_row['state_id']

            # 3.--- Cargar ciudades del país seleccionado ---
            df_cities = cargar_ciudades()
            df_cities = df_cities[df_cities['state_id'] == state_id]
            df_cities['area_km2'] = df_cities['area_km2'].round(1)

            if not df_cities.empty:
                st.subheader(f"Ciudades en {selected_state}")

                # Layer de ciudades del país
                city_layer = pdk.Layer(
                    "PolygonLayer",
                    data=df_cities,
                    get_polygon="coordinates",
                    get_fill_color="[30, 30, 200, 150]",  # azul
                    get_line_color="[0, 0, 0, 255]",
                    line_width_min_pixels=1,
                    pickable=True,
                    extruded=False,
                )

                tooltip_cities = {
                    "html": "<b>Ciudad:</b> {city_name}<br/><b>Área:</b> {area_km2} km²",
                    "style": {"backgroundColor": "blue", "color": "white"}
                }


                # Centrar en el país
                state_center = calcular_centro(state_row['coordinates'])

                state_contour_layer = pdk.Layer(
                "PolygonLayer",
                data=state_row.to_frame().T,  # país seleccionado
                get_polygon="coordinates",
                get_fill_color="[0, 0, 0, 0]",  # sin relleno (completamente transparente)
                get_line_color="[0, 0, 0, 255]",  # borde negro
                line_width_min_pixels=2,
                pickable=False,  # no necesitas tooltip para el contorno
                extruded=False,
    )
                layers = [state_contour_layer, city_layer]
                st.pydeck_chart(pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state=pdk.ViewState(
                        latitude=state_center.y,
                        longitude=state_center.x,
                        zoom=5,
                        pitch=0,
                    ),
                    layers=layers,
                    tooltip=tooltip_cities
                ))

                if st.checkbox(f"Mostrar tabla de las ciudades de {selected_state}"):
                    st.dataframe(df_cities)


                # 4. Seleccionar ciudad del país
                selected_city = st.selectbox("Selecciona una ciudad:", df_cities['city_name'].unique())

                if selected_city:
                    city_row = df_cities[df_cities['city_name'] == selected_city].iloc[0]
                    city_id = city_row['city_id']

                    df_parcels = cargar_parcels()

                    if not df_parcels.empty:
                        st.subheader(f"Parcelas en {selected_city}")

                        parcels_layer = pdk.Layer(
                            "PolygonLayer",
                            data=df_parcels,
                            get_polygon="coordinates",
                            get_fill_color="[0, 200, 100, 150]",  # verde
                            get_line_color="[0, 0, 0, 255]",
                            line_width_min_pixels=1,
                            pickable=True,
                            extruded=False,
                        )

                        tooltip_parcels = {
                            "html": "<b>Área:</b> {area_m2} m²",
                            "style": {"backgroundColor": "green", "color": "white"}
                        }

                        # Centrar en la ciudad
                        city_center = calcular_centro(city_row['coordinates'])

                        st.pydeck_chart(pdk.Deck(
                            map_style="mapbox://styles/mapbox/light-v9",
                            initial_view_state=pdk.ViewState(
                                latitude=city_center.y,
                                longitude=city_center.x,
                                zoom=11,
                                pitch=0,
                            ),
                            layers=[parcels_layer],
                            tooltip=tooltip_parcels
                        ))

                        if st.checkbox(f"Mostrar tabla de parcelas en {selected_city}"):
                            st.dataframe(df_parcels[df_parcels['city_id'] == city_id])
                    else:
                        st.warning("Esta ciudad no tiene parcelas registradas.")
            else:
                st.warning("Este país no tiene ciudades registradas.")
    else:
        st.error("No se pudieron cargar los estados.")