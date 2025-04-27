import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.neighbors import NearestNeighbors


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, '..', 'datasetIncluido', 'spotify_tracks_with_personality.csv')

df = pd.read_csv(csv_path)


# Preprocesamiento
df['explicit'] = df['explicit'].astype(int)

le = LabelEncoder()
df['personality_encoded'] = le.fit_transform(df['personality'])

features = ['energy', 'danceability', 'explicit', 'personality_encoded']
X = df[features]

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Entrenar modelo KNN
knn = NearestNeighbors(n_neighbors=1, metric='euclidean')
knn.fit(X_scaled)

def recomendar_cancion(energy, danceability, explicit, personality_text):
    """
    Recomienda una canción basada en parámetros dados.
    """
    personality_encoded = le.transform([personality_text])[0]
    
    user_input = np.array([[energy, danceability, int(explicit), personality_encoded]])
    
    user_input_scaled = scaler.transform(user_input)
    
    distancia, indice = knn.kneighbors(user_input_scaled)
    
    recomendacion = df.iloc[indice[0][0]]
    
    resultado = {
        'track_name': recomendacion['track_name'],
        'artist': recomendacion['artists'],
        'album_name': recomendacion['album_name'],
        'genre': recomendacion['track_genre']
    }
    
    return resultado
