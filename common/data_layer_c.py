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

def roads():
    query = '''
    SELECT
        r.id AS road_id,
        r.origin_city_id,
        origin_city.name AS origin_city_name,
        r.target_city_id,
        target_city.name AS target_city_name,
        r.toll,
        r.length_km,
        r.geometry
    FROM
        roads r
    JOIN
        cities origin_city ON r.origin_city_id = origin_city.id
    JOIN
        cities target_city ON r.target_city_id = target_city.id;

    '''
    df = pd.read_sql(query, engine)
    return df

def rental_vehicles():
    query = '''
    SELECT
        v.id AS vehicle_id,
        v.city_id,
        c.name AS city_name,
        v.rental_cost_per_hour,
        v.vin,
        v.model_year,
        v.make,
        v.model,
        v.electric_range,
        v.capacity,
        v.type
    FROM
        electric_rental_vehicle v
    JOIN
        cities c ON v.city_id = c.id;

    '''
    df = pd.read_sql(query, engine)
    return df
