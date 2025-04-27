from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

def cargar_cities():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM cities;"""
    df = pd.read_sql(query, engine)
    return df


# --- Gym ---
def cargar_gym():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Gym';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_gym"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

# --- Venue ---
def cargar_venue():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Venues';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_venues"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

@st.cache
# --- Restaurant ---
def cargar_restaurant():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Restaurant';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_restaurant"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

# 

# --- Park ---
def cargar_park():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Park';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_park"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

# --- Religious Building ---
def cargar_religious_building():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Religious Building';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_religious_building"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

# --- Hotel ---
def cargar_hotel():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Hotel';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_hotel"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df