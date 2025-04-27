import streamlit as st
import pandas as pd
import requests
from shapely import wkb
import datetime
import networkx as nx

# Carga de datos de la API
@st.cache_data
def cargar_roads():
    url = "http://localhost:8080/api/roads"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    else:
        st.error("No se pudieron cargar los datos de la API.")

@st.cache_data
def cargar_vehiculos():
    url = "http://localhost:8080/api/rental_vehicles"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    else:
        st.error("No se pudieron cargar los datos de la API.")

df_roads = cargar_roads()
df_roads = df_roads.rename(columns={
    'road_id': 'ID Carretera',
    'origin_city_name': 'Ciudad de origen',
    'target_city_name': 'Ciudad de destino',
    'origin_city_id': 'ID ciudad de origen',
    'target_city_id': 'ID ciudad de destino',
    'toll': 'Peaje',
    'length_km': 'Longitud(km)',
    'geometry': 'Geometria'
})
df_vehiculos = cargar_vehiculos()
df_vehiculos = df_vehiculos.rename(columns={
    'vehicle_id': 'ID Vehiculo',
    'city_id': 'ID Ciudad',
    'city_name': 'Ciudad',
    'make': 'Marca',
    'model': 'Modelo',
    'rental_cost_per_hour': 'Precio/hora',
    'electric_range': 'Autonomia(km)',
    'capacity': 'Capacidad',
    'type': 'Tipo',
    'model_year': 'Año de fabricacion',
})

# Funciones auxiliares
def convertir_geometry_wkb(geometry_hex):
    geom = wkb.loads(bytes.fromhex(geometry_hex))
    if geom.geom_type == "LineString":
        return list(geom.coords)
    else:
        return None
    
def extraer_inicio_fin(geometry_hex):
    geom = wkb.loads(bytes.fromhex(geometry_hex))
    if geom.geom_type == "LineString":
        coords = list(geom.coords)
        return coords[0], coords[-1]  # inicio, fin
    else:
        return None, None
    
def construir_grafo(df_roads):
    G = nx.DiGraph()  # Grafo dirigido (origen ➔ destino)

    for _, row in df_roads.iterrows():
        origen = row['Ciudad de origen']
        destino = row['Ciudad de destino']
        distancia = row['Longitud(km)']

        G.add_edge(origen, destino, weight=distancia)

    return G

def encontrar_camino_mas_corto(G, origen, destino):
    try:
        camino = nx.shortest_path(G, origen, destino, weight='weight')
        return camino
    except nx.NetworkXNoPath:
        return None

def calcular_distancia_total(df_roads, camino):
    distancia_total = 0

    # Recorremos el camino de dos en dos (origen ➔ destino)
    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i + 1]

        # Buscar la fila que conecta origen con destino
        ruta = df_roads[
            (df_roads['Ciudad de origen'] == origen) &
            (df_roads['Ciudad de destino'] == destino)
        ]

        if not ruta.empty:
            distancia_total += ruta.iloc[0]['Longitud(km)']
        else:
            st.warning(f"No se encontró ruta entre {origen} y {destino}.")

    return distancia_total

def construir_texto_camino(camino_encontrado):
    texto_camino = ""

    for i in range(len(camino_encontrado) - 1):
        origen = camino_encontrado[i]
        destino = camino_encontrado[i + 1]

        if G.has_edge(origen, destino):
            km = G[origen][destino]['weight']
            texto_camino += f"{origen} ➔ ({km:.1f} km) ➔ "
        else:
            texto_camino += f"{origen} ➔ (sin datos) ➔ "

    # Añadir la última ciudad
    texto_camino += camino_encontrado[-1]

    return texto_camino



# Flujo de la aplicación   
opcion = st.radio(
    "¿Qué quieres hacer?",
    ("Ver tablas de datos disponibles", "Conoce las rutas desde tu ciudad", "Servicios de alquiler de vehículos")
)

if opcion == "Ver tablas de datos disponibles":
    st.header("Tablas de Datos")

    if st.checkbox("Mostrar tabla de carreteras"):
        st.dataframe(df_roads.drop(columns=['ID ciudad de origen', 'ID ciudad de destino']))

    if st.checkbox("Mostrar tabla de vehículos de alquiler"):
        st.dataframe(df_vehiculos.drop(columns=['ID Ciudad']))

if opcion == "Conoce las rutas desde tu ciudad":
    st.header("🚗 🗺️  Explorador de Rutas")

    if not df_roads.empty and not df_vehiculos.empty:
        G = construir_grafo(df_roads)

        st.subheader("🧭 Ruta más corta entre dos ciudades")
        st.write("Selecciona la ciudad de origen y destino, y si existe, te proporcionaremos la ruta más corta.")

        # Listas de ciudades únicas
        ciudades_origen = df_roads['Ciudad de origen'].unique()
        ciudades_destino = df_roads['Ciudad de destino'].unique()

        origen = st.selectbox("Ciudad de origen:", sorted(ciudades_origen))
        destino = st.selectbox("Ciudad de destino:", sorted(ciudades_destino))

        # 2. Encontrar camino más corto
        camino_encontrado = encontrar_camino_mas_corto(G, origen, destino)

        if camino_encontrado:

            st.success(f"Camino encontrado: {construir_texto_camino(camino_encontrado)}")

            # 3. Calcular distancia total
            distancia_total = calcular_distancia_total(df_roads, camino_encontrado)
            st.info(f"Distancia total del recorrido: {distancia_total:.2f} km")
        else:
            st.error("No hay rutas disponibles entre esas dos ciudades")

        st.subheader("🧭 Rutas directas desde tu ciudad")
        st.write("Selecciona la ciudad de origen y te proporcionamos los destinos posibles mediante una ruta directa y su información.")

        origen2 = st.selectbox("Ciudad origen:", sorted(ciudades_origen))
     
        if origen2:
            # Filtrar las rutas que tienen ese origen
            rutas_desde_origen = df_roads[df_roads['Ciudad de origen'] == origen2]

            # Listado de destinos posibles desde ese origen
            destinos_posibles = rutas_desde_origen['Ciudad de destino'].unique()

            destino2 = st.selectbox("Ciudad destino:", sorted(destinos_posibles))

            if destino2:
                # Ahora filtrar rutas específicas de origen ➔ destino
                rutas_disponibles = rutas_desde_origen[
                    rutas_desde_origen['Ciudad de destino'] == destino2
                ].reset_index(drop=True)

                if not rutas_disponibles.empty:
        
                    ruta_info = rutas_disponibles.loc[0]
                    longitud_ruta = ruta_info['Longitud(km)'].round(2)
                    peaje = ruta_info['Peaje']
                    st.success(f'Ruta disponible de {longitud_ruta} km y peaje de {peaje} €')


            # Preguntar si quiere ver los vehículos
            st.subheader("¿Necesitas medio de transporte?")
            if st.checkbox("¿Quieres ver los vehículos de alquiler disponibles en tu ciudad?"):

                st.write("Introduce los km de tu ruta y te enseñaremos los vehículos eléctricos disponibles con suficiente autonomía.")
                km_ruta = st.number_input(
                    "Introduce la distancia de tu ruta (km):",
                    min_value=0.0,
                    max_value=1000.0,
                    value=100.0,  # valor inicial
                    step=0.5  # pasos de 0.5 km
)
                st.subheader("Vehículos eléctricos disponibles")

                vehiculos_con_autonomia = df_vehiculos[
                    (df_vehiculos['Ciudad'] == origen) &
                    (df_vehiculos['Autonomia(km)'] >= km_ruta)
                ].reset_index(drop=True)

                if not vehiculos_con_autonomia.empty:
                    tipos_disponibles = vehiculos_con_autonomia['Tipo'].dropna().unique()
                    tipo_seleccionado = st.selectbox(
                        "Filtra por tipo de vehículo:", 
                        ["Todos"] + sorted(tipos_disponibles)
                    )

                    if tipo_seleccionado != "Todos":
                        vehiculos_con_autonomia = vehiculos_con_autonomia[
                            vehiculos_con_autonomia['Tipo'] == tipo_seleccionado
                        ]

                    # Mostrar tabla final
                    st.dataframe(vehiculos_con_autonomia[['ID Vehiculo','Marca', 'Modelo', 'Precio/hora', 'Autonomia(km)', 'Capacidad', 'Tipo']])
                    opciones_vehiculos = [
                        f"{idx} - {row['Marca']} {row['Modelo']} ({row['Autonomia(km)']} km autonomía)"
                        for idx, row in vehiculos_con_autonomia.iterrows()
                    ]

                    # Mostrar el selectbox con las opciones bonitas
                    opcion_selec = st.selectbox(
                        "Selecciona el vehículo:",
                        opciones_vehiculos )
                    
                    indice_vehiculo_seleccionado = int(opcion_selec.split(' - ')[0])
                    vehiculo_info = vehiculos_con_autonomia.loc[indice_vehiculo_seleccionado]

                    st.success(f"Has seleccionado el vehículo: {indice_vehiculo_seleccionado} de {vehiculo_info['Marca']} {vehiculo_info['Modelo']}")
                    st.subheader("Introduce tus fechas de alquiler y te calculamos el precio")
                    # Pedir fechas
                    fecha_recogida = st.date_input("Fecha de recogida")
                    hora_recogida = st.time_input("Hora de recogida")
                    datetime_recogida = datetime.datetime.combine(fecha_recogida, hora_recogida)
                    
                    fecha_devolucion = st.date_input("Fecha de devolución")
                    hora_devolucion = st.time_input("Hora de devolución")
                    datetime_devolucion = datetime.datetime.combine(fecha_devolucion, hora_devolucion)
                    # Validar y calcular precio
                    if datetime_devolucion <= datetime_recogida:
                        st.error("La fecha de devolución debe ser posterior a la de recogida.")
                    else:
                        duracion_horas = (datetime_devolucion - datetime_recogida).total_seconds() / 3600
                        duracion_horas = round(duracion_horas, 2)

                        precio_total = vehiculo_info['Precio/hora'] * duracion_horas

                        st.success(f"Duración del alquiler: {duracion_horas:.2f} horas")
                        st.success(f"Precio total: {precio_total:.2f} €")


                else:
                    st.warning("No hay vehículos de alquiler con autonomía suficiente para esta ruta. Perdone las molestias.")

                    

if opcion == "Servicios de alquiler de vehículos":
    st.header("🚗 Servicios de Alquiler de Vehículos")
    st.write("Explora los vehículos eléctricos disponibles en todas las ciudades. Aplica los filtros que se adapten a tus necesidades y conoce el precio total de tu alquiler.")

    ciudades = df_vehiculos['Ciudad'].unique()
    ciudad_seleccionada = st.selectbox("Selecciona una ciudad:", sorted(ciudades))
    if ciudad_seleccionada:
        vehiculos_ciudad = df_vehiculos[df_vehiculos['Ciudad'] == ciudad_seleccionada].reset_index(drop=True)

        if not vehiculos_ciudad.empty:
            # Crear contenedor para los filtros
            with st.expander("🔎 Filtrar vehículos"):
                # Filtrar por tipo
                tipos_disponibles = vehiculos_ciudad['Tipo'].dropna().unique()
                tipo_seleccionado = st.multiselect(
                    "Selecciona tipo(s) de vehículo:",
                    opciones := sorted(tipos_disponibles),
                    default=opciones
                )

                # Filtrar por capacidad
                capacidad_min, capacidad_max = int(vehiculos_ciudad['Capacidad'].min()), int(vehiculos_ciudad['Capacidad'].max())
                capacidad_seleccionada = st.slider(
                    "Capacidad mínima del vehículo:",
                    min_value=capacidad_min,
                    max_value=capacidad_max,
                    value=capacidad_min
                )

                # Filtrar por precio máximo por hora
                precio_min, precio_max = vehiculos_ciudad['Precio/hora'].min(), vehiculos_ciudad['Precio/hora'].max()
                precio_maximo = st.slider(
                    "Precio máximo por hora (€):",
                    min_value=float(precio_min),
                    max_value=float(precio_max),
                    value=float(precio_max)
                )

                # Filtrar por autonomía mínima
                autonomia_min, autonomia_max = vehiculos_ciudad['Autonomia(km)'].min(), vehiculos_ciudad['Autonomia(km)'].max()
                autonomia_minima = st.slider(
                    "Autonomía mínima requerida (km):",
                    min_value=float(autonomia_min),
                    max_value=float(autonomia_max),
                    value=float(autonomia_min)
                )

            # --- Aplicar los filtros ---
            df_filtrado = vehiculos_ciudad[
                (vehiculos_ciudad['Tipo'].isin(tipo_seleccionado)) &
                (vehiculos_ciudad['Capacidad'] >= capacidad_seleccionada) &
                (vehiculos_ciudad['Precio/hora'] <= precio_maximo) &
                (vehiculos_ciudad['Autonomia(km)'] >= autonomia_minima)
            ]

            if not df_filtrado.empty:
                st.subheader("📅 Introduce fechas de alquiler")
                st.write("Selecciona las fechas de recogida y devolución para calcular el precio total del alquiler.")

                # 2. Introducir fechas y calcular duración
                fecha_recogida = st.date_input("Fecha de recogida")
                hora_recogida = st.time_input("Hora de recogida")
                datetime_recogida = datetime.datetime.combine(fecha_recogida, hora_recogida)

                fecha_devolucion = st.date_input("Fecha de devolución")
                hora_devolucion = st.time_input("Hora de devolución")
                datetime_devolucion = datetime.datetime.combine(fecha_devolucion, hora_devolucion)

                if datetime_devolucion <= datetime_recogida:
                    st.error("La fecha de devolución debe ser posterior a la de recogida.")
                else:
                    duracion_horas = (datetime_devolucion - datetime_recogida).total_seconds() / 3600
                    duracion_horas = round(duracion_horas, 2)

                    st.success(f"Duración del alquiler: {duracion_horas:.2f} horas")

                    # 3. Calcular precio total para cada vehículo
                    df_filtrado['Precio total(€)'] = (df_filtrado['Precio/hora'] * duracion_horas).round(2)

                    # 4. Mostrar tabla
                    st.subheader("🚗 Vehículos disponibles")
                    st.dataframe(df_filtrado[['Marca', 'Modelo', 'Precio/hora', 'Autonomia(km)', 'Capacidad', 'Tipo', 'Año de fabricacion', 'Precio total(€)']])

            else:
                st.warning("No hay vehículos que cumplan con esos filtros.")


        else:
            st.warning(f"No hay vehículos disponibles en {ciudad_seleccionada}.")


