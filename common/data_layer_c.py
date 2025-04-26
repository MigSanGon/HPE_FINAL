from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )
def estado_fronteras():

    query = ''' SELECT 
                    s.id AS state_id,
                    s.name AS state_name,
                    sb.vertices,
                    sb.bounding_box,
                    sb.area_km2
                FROM 
                    states s
                JOIN 
                    state_borders sb ON s.id = sb.state_id;'''
    df = pd.read_sql(query, engine)
    
    return df

def ciudad_fronteras():
    query = ''' SELECT 
                    c.id AS city_id,
                    c.name AS city_name,
                    c.state_id,
                    cb.vertices,
                    cb.bounding_box,
                    cb.area_km2
                FROM 
                    cities c
                JOIN 
                    city_borders cb ON c.id = cb.city_id;
    '''
    df = pd.read_sql(query, engine)
    
    return df

def parcels():
    query = '''
    SELECT
        p.city_id,
        c.name AS city_name,
        p.parcel_id,
        p.vertices,
        p.area_m2,
        p.centroid_lat,
        p.centroid_lon
    FROM
        parcels p
    JOIN
        cities c ON p.city_id = c.id;
    '''
    df = pd.read_sql(query, engine)
    return df
