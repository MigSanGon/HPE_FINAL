from sqlalchemy import create_engine
import pandas as pd

def cargar_cities():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM cities;"""
    df = pd.read_sql(query, engine)
    return df

def cargar_dayc():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Daycare';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_daycare"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

def cargar_pet():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Pet Services';"""
    df1 = pd.read_sql(query, engine)
    query = """SELECT *
    FROM 
        infrastructure_pet_services;"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df


def cargar_seni():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Senior Living';"""
    df1 = pd.read_sql(query, engine)
    query = """SELECT *
    FROM 
        infrastructure_senior_living"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    
    return df

def cargar_event_s():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        events
    WHERE senior_discount_available =
            TRUE;"""
    df = pd.read_sql(query, engine)
   
    
    return df

def cargar_event_c():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        events
    WHERE is_family_friendly =
            TRUE;"""
    df = pd.read_sql(query, engine)
    
    
    return df