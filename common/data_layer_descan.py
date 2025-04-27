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

# --- School ---
def cargar_school():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'School';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_school"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

# --- Office Building ---
def cargar_office_building():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Office Building';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_office_building"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

# --- Bank ---
def cargar_bank():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Bank';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_bank"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

# --- Transportation Hub ---
def cargar_transportation_hub():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Transportation Hub';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_transportation_hub"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

# --- Laundromat ---
def cargar_laundromat():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Laundromat';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_laundromat"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

# --- Salon ---
def cargar_salon():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Salon';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_salon"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

# --- Government Building ---
def cargar_government_building():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Government Building';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_government_building"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df

# --- Fabric ---
def cargar_fabric():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM 
        infrastructure
    WHERE type =
            'Fabric';"""
    df1 = pd.read_sql(query, engine)

    query = """SELECT *
    FROM 
        infrastructure_fabric"""
    df = pd.read_sql(query, engine)
    df = df.merge(
        df1,         
        left_on='infra_id',           
        right_on='id',                 
        how='inner'                     
    )
    return df
