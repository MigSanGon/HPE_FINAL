from sqlalchemy import create_engine
import pandas as pd

def cargar_cities1():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM cities;"""
    df = pd.read_sql(query, engine)
    return df

def cargar_med():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Hospital';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_hospital"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

def cargar_clin():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Healthcare Clinic';"""
    df1 = pd.read_sql(query, engine)
    query = """SELECT *
    FROM 
        infrastructure_healthcare_clinic"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df


def cargar_phar():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Pharmacy';"""
    df1 = pd.read_sql(query, engine)
    query = """SELECT *
    FROM 
        infrastructure_pharmacy"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    
    return df
