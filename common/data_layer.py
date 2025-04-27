from sqlalchemy import create_engine
import pandas as pd

def cargar_cities():
    engine = create_engine(
        'postgresql+psycopg2://admin:loYo1HT25@10.10.76.244:6565/greenlake_data'
    )

    query = """SELECT *
    FROM infrastructure_gym;"""
    df = pd.read_sql(query, engine)
    
    return df

df=cargar_cities()
print(df)