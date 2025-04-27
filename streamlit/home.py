import streamlit as st


 # --- CSS personalizado para los botones ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #dfe9f3, #ffffff);
        font-family: 'Segoe UI', sans-serif;
    }
    div.stButton > button {
        background-color: #42a5f5;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #42a5f5;
        color: #f0f0f0;
    }
                
    div.stButton > button:focus {
        color: black !important;
        background-color: #4CAF50 !important;
        font-weight: bold !important;
        outline: none;
    }
                
        
    </style>
    """, unsafe_allow_html=True)

# Inicializar página actual
if "page" not in st.session_state:
    st.session_state.page = "home"

# Función para cambiar de página
def change_page(page_name):
    st.session_state.page = page_name


if st.session_state.page == "home":
    st.title("Data GLake ⛰️")
    st.markdown('''##### Bienvenido al portal de datos de GreenLake. Tendrás a tu disposición tablas de datos '''
    ''' específicas con un buscador y una pestaña para descargar en formato CSV. Analiza los datos a tu gusto. '''
    ''' También se añaden funcionalidades a partir de los datos para hacer la información de GreenLake accesible a todos 🌍 ''')

    st.markdown("---")  

    if st.button("GreenLake Vibes🎙️"):
        change_page("music")

    if st.button(" 🗺️ GreenLake Maps 🗺️ "):
        change_page("mapas")

    if st.button("🚗 🗺️  Explorador de Rutas"):
        change_page("rutas")

    if st.button("🏢 Infraestructuras para usuario 🏫"):
        change_page("infra")
    
    if st.button(" 🩺 Salud 💊 ", key="button_salud"):
        change_page("salud")

    if st.button("👶 Asistencia 🐶", key="button_asistencia"):
        change_page("asis")

    if st.button("🛒 Compras 🚐", key="button_compras"):
        change_page("compra")

   


elif st.session_state.page == "music":
    from music import app
    app(change_page)

elif st.session_state.page == "mapas":
    from borders import app
    app(change_page)

elif st.session_state.page == "rutas":
    from roads import app
    app(change_page)

elif st.session_state.page == "infra":
    from app_descan import app
    app(change_page)

elif st.session_state.page == "salud":
    from app_med import app
    app(change_page)

elif st.session_state.page == "asist":
    from app_asist import app
    app(change_page)

elif st.session_state.page == "compra":
    from app_supply import app
    app(change_page)