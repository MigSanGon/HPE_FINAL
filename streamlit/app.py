import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from knn import recomendar_cancion


# Estado de la sesión para recordar la página
if 'pagina' not in st.session_state:
    st.session_state.pagina = 1


st.set_page_config(page_title="Visualización de People", layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #000000;'>GreenLake Vibes🎙️</h1>",
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

st.subheader("¡Encuentra a gente afín a ti y descubre sus gustos musicales! 🎧🎶")

# Tamaño de página
limit = 100
skip = (st.session_state.pagina - 1) * limit

url = f"http://localhost:8080/api/greenlake-eval/people?skip={skip}&limit={limit}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)

    # --- Calcular Edad ---
    if 'birth_date' in df.columns:
        df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
        today = pd.to_datetime('today')
        df['Edad'] = df['birth_date'].apply(lambda x: today.year - x.year - ((today.month, today.day) < (x.month, x.day)) if pd.notnull(x) else None)
        df = df.drop(columns=['birth_date'])

    # --- Renombrar columnas ---
    df = df.rename(columns={
        'first_name': 'Nombre',
        'last_name': 'Apellidos',
        'job_sector': 'Trabajo',
        'city_name': 'Ciudad',
        'education': 'Educación',
        'personality': 'Personalidad',
        'track_names': 'Canciones favoritas'
    })

    # --- Reordenar columnas ---
    cols = list(df.columns)
    if 'Edad' in cols:
        cols.insert(cols.index('Apellidos') + 1, cols.pop(cols.index('Edad')))
    df = df[cols]

    # --- Filtros en el flujo principal ---

    # --- Filtros en el flujo principal ---
    st.markdown(
    "#### 🤝 **Filtra para encontrar a personas que mejor encajen contigo**\n\n"
    "##### ¿Quieres conocer a gente que comparta tus gustos musicales y otros intereses? "
    "Utiliza nuestro sistema de filtros para encontrar personas que conecten contigo. "
    "Busca usuarios por ciudad, edad, educación o incluso por trabajo... ¿A qué esperas para empezar a conocer a gente? 😎"
)



    # Filtro Edad
    # Título bonito del slider
    st.markdown("#### 📅 **Selecciona el rango de edad**")

    # Slider de edad sin texto encima
    min_edad = int(df['Edad'].min()) if not df['Edad'].isnull().all() else 18
    max_edad = int(df['Edad'].max()) if not df['Edad'].isnull().all() else 99
    edad_range = st.slider(
        label="Selecciona el rango de edad:",  # Deja un label aunque no se vea
        min_value=18,
        max_value=99,
        value=(min_edad, max_edad),
        label_visibility="collapsed"  # 👈 Eliminar espacio reservado
    )


    st.markdown("#### 📍 **Selecciona una ciudad**")

    ciudades = df['Ciudad'].dropna().unique().tolist()
    ciudades_seleccionadas = st.multiselect(
        label="Selecciona ciudades:",  # Puedes dejar el label real, no importa
        options=sorted(ciudades),
        default=[],
        label_visibility="collapsed"  
    )

    # Filtro Educación

    st.markdown("#### 📚 **Selecciona una titulación**")

    educaciones = df['Educación'].dropna().unique().tolist()
    educaciones_seleccionadas = st.multiselect(
        label="Selecciona niveles de educacion:",  # Puedes dejar el label real, no importa
        options=sorted(educaciones),
        default=[],
        label_visibility="collapsed"  #
    )


    # Filtro Trabajo

    st.markdown("#### 💼 **Selecciona un trabajo**")

    trabajos = df['Trabajo'].dropna().unique().tolist()
    trabajos_seleccionados = st.multiselect(
        label="Selecciona sector laboral:",  # Etiqueta (aunque no se verá)
        options=sorted(trabajos),
        default=[],
        label_visibility="collapsed"  # Para no dejar espacio de label
    )


    # --- Aplicar Filtros ---
    df_filtrado = df[
        (df['Edad'] >= edad_range[0]) & (df['Edad'] <= edad_range[1])
    ]

    if ciudades_seleccionadas:
        df_filtrado = df_filtrado[df_filtrado['Ciudad'].isin(ciudades_seleccionadas)]

    if educaciones_seleccionadas:
        df_filtrado = df_filtrado[df_filtrado['Educación'].isin(educaciones_seleccionadas)]

    if trabajos_seleccionados:
        df_filtrado = df_filtrado[df_filtrado['Trabajo'].isin(trabajos_seleccionados)]


    # --- Mostrar tabla filtrada ---
    st.dataframe(df_filtrado)

    # --- Paginación debajo de la tabla ---
    col1, col2, col3 = st.columns([1, 2, 1])  # Más pegaditos

    with col1:
        if st.button("⬅️ Anterior"):
            if st.session_state.pagina > 1:
                st.session_state.pagina -= 1

    with col2:
        st.markdown(f"<h5 style='text-align: center;'>Página {st.session_state.pagina}</h5>", unsafe_allow_html=True)

    with col3:
        if st.button("Siguiente ➡️"):
            if len(df) == limit:  # Solo avanzar si hay más datos
                st.session_state.pagina += 1


else:
    st.error("No se pudieron cargar los datos de la API.")


# --- Sistema Recomendador de Canciones ---
st.markdown("<br><hr><br>", unsafe_allow_html=True)
st.markdown("## 🎶 Encuentra tu canción perfecta")

st.markdown(
    "##### ¿Quieres descubrir tu nueva canción preferida? Nosotros lo hacemos por ti 😎 \n\n"
    "Responde a 4 preguntas acerca de ti para que te conozcamos más y nuestro algoritmo de IA te recomendará tu canción ideal seguń tu personalidad. "
)



# Sliders para parámetros
# --- Slider de Energy ---
st.markdown("#### ¿Cuánta energía quieres en tus canciones? ⚡")
energy_visible = st.slider(
    label="Nivel de energía",
    min_value=0,
    max_value=10,
    value=5,
    step=1,
    label_visibility="collapsed" 
)

energy = energy_visible / 10  

# --- Slider de Danceability ---
st.markdown("#### ¿Qué tan bailable quieres que sea la canción? 🕺")
danceability_visible = st.slider(
    label="Nivel de bailabilidad",
    min_value=0,
    max_value=10,
    value=5,
    step=1,
    label_visibility="collapsed" 
)

danceability = danceability_visible / 10  

st.markdown("#### **¿Quieres que tu canción sea explícita? 🔥**")
explicit = st.selectbox(
    label="¿Quieres que sea explícita?",  
    options=[False, True],
    format_func=lambda x: "Sí" if x else "No",
    label_visibility="collapsed"  
)


# Cargar personalidades (mismo listado que usaste en el KNN)
personalidades = [
    "Determined", "Progressive", "Calm", "Reserved", "Traditional",
    "Adventurous", "Disciplined", "Resourceful", "Innovative", "Resilient",
    "Energetic", "Outgoing", "Community-oriented", "Analytical", "Adaptable",
    "Cooperative", "Practical", "Creative", "Curious", "Independent", "Patient"
]

st.markdown("#### **Selecciona que adjetivo describe mejor tu personalidad**")
personality = st.selectbox(
    label = "Selecciona tu tipo de personalidad",
    options=sorted(personalidades),
    label_visibility="collapsed"  
)

# Botón para recomendar
# Botón bonito usando HTML
# Botón bonito con hover negro
# Botón bonito: letras negras al pasar el ratón
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #42a5f5; /* azul normal */
        color: white; /* letras blancas por defecto */
        height: 50px;
        width: 100%;
        border-radius: 12px;
        border: none;
        font-size: 18px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #1e88e5; /* azul más oscuro al pasar el ratón */
        color: black; /* 👈 letras negras al hacer hover */
    }
    </style>
""", unsafe_allow_html=True)



# Ahora el botón real
if st.button("🎵 Recomendar canción"):
    resultado = recomendar_cancion(
        energy=energy,
        danceability=danceability,
        explicit=explicit,
        personality_text=personality
    )
    

    
    st.markdown("""
    <div style="background-color:#e3f2fd; padding:25px; border-radius:12px; border:1px solid #90caf9;">
        <h2 style="font-size:28px;">🎵 Tu canción recomendada</h2>
        <ul style="font-size:20px; line-height:1.8;">
            <li><strong>🎼 Título:</strong> {track_name}</li>
            <li><strong>🎤 Artista:</strong> {artist}</li>
            <li><strong>💿 Álbum:</strong> {album_name}</li>
            <li><strong>🎶 Género:</strong> {genre}</li>
        </ul>
    </div>
""".format(
    track_name=resultado['track_name'],
    artist=resultado['artist'],
    album_name=resultado['album_name'],
    genre=resultado['genre']
), unsafe_allow_html=True)
