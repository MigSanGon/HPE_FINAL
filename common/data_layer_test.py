from sqlalchemy import create_engine
import pandas as pd

def test_hospital(longitude,latitude, radius=1000):
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = f"""SELECT id,city_id,name,
    ST_X(location) AS longitude,
    ST_Y(location) AS latitude,
    ST_Distance(location, ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326)::geography) AS distance
    FROM infrastructure
    WHERE type = 'Hospital' AND ST_DWithin(
        location, 
        ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326)::geography,{radius});"""
    
    df = pd.read_sql(query, engine)
    
    return df