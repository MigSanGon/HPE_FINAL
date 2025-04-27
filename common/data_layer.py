from sqlalchemy import create_engine, text
import pandas as pd

# Crear la conexión global
engine = create_engine(
    'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
)

def cargar_people_enriquecido(skip=0, limit=100):
    """
    Carga datos de personas con ciudad y músicas agrupadas en una columna, usando paginación SQL directa.
    """
    query = text(f"""
        SELECT 
            p.first_name,
            p.last_name,
            p.job_sector,
            c.name AS city_name,
            p.birth_date,
            p.education,
            p.personality,
            STRING_AGG(m.track_name, ', ') AS track_names
        FROM people p
        LEFT JOIN cities c ON p.city_id = c.id
        LEFT JOIN people_music pm ON p.id = pm.people_id
        LEFT JOIN music m ON pm.music_id = m.id
        GROUP BY 
            p.id, p.first_name, p.last_name, p.job_sector, 
            p.employment_status, p.income, c.name, 
            p.birth_date, p.education, p.personality
        OFFSET {skip}
        LIMIT {limit}
    """)
    df = pd.read_sql(query, engine)
    return df



def obtener_hospitales_cercanos(lat, lon, radius=1000):
    query = text(f"""
        SELECT
        id,
        city_id,
        name,
        ST_X(location) AS longitude,
        ST_Y(location) AS latitude,
        ST_Distance(location::geography, ST_MakePoint(:lon, :lat)::geography) AS distance_m
    FROM infrastructure
    WHERE type = 'Hospital'
    AND ST_DWithin(location::geography, ST_MakePoint(:lon, :lat)::geography, :radius)
    ORDER BY distance_m ASC;

    """)

    with engine.connect() as connection:
        result = connection.execute(query, {"lat": lat, "lon": lon, "radius": radius})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    return df