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

def cargar_shop():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Shop';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_shop"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

def cargar_gas():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Gas Station';"""
    df1 = pd.read_sql(query, engine)
    query = """SELECT *
    FROM 
        infrastructure_gas_station;"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df


def cargar_super():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Supermarket';"""
    df1 = pd.read_sql(query, engine)
    query = """SELECT *
    FROM 
        infrastructure_supermarket"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    
    return df

def cargar_auto():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Auto Service';"""
    df1 = pd.read_sql(query, engine)
    query = """SELECT *
    FROM 
        infrastructure_auto_service"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    
    return df