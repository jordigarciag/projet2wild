# bibliothèques
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler

# Chargement des données
urlt = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/tconst.tsv.gz"
df_movies = pd.read_csv(urlt, sep='\t')

# Nettoyage des genres et ajout de la colonne budget (avec des valeurs par défaut)
df_movies['genres'] = df_movies['genres'].fillna('Sans catégorie')
df_movies['genres'] = df_movies['genres'].apply(lambda x: x.replace("'","").replace("[","").replace("]","").split(","))
df_movies['genres'] = df_movies['genres'].apply(lambda x: list(filter(None, [ele.strip() for ele in x])))
df_movies['budget'] = df_movies['budget'].fillna(df_movies['budget'].mean())  # on remplit les valeurs manquantes avec la moyenne

# Utilisation de get_dummies pour le one-hot encoding des genres
genres_dummies = pd.get_dummies(df_movies['genres'].explode()).groupby(level=0).sum()
df_movies = pd.concat([df_movies, genres_dummies], axis=1)

# Préparation des features
numeric_features = ['rate', 'year', 'runtimeMinutes', 'budget']
genre_columns = genres_dummies.columns.tolist()
feature_columns = numeric_features + genre_columns

# Préparation du dataset pour le modèle
X = df_movies[feature_columns].copy()
X = X.fillna(0)

# Normalisation des features numériques
scaler = MinMaxScaler()
X[numeric_features] = scaler.fit_transform(X[numeric_features])

# Modèle KNN
model = NearestNeighbors(n_neighbors=5, metric='euclidean')
model.fit(X)

def get_movie_recommendations(rate, year, runtime, budget, selected_genre, df=df_movies, model=model, scaler=scaler):
    input_features = np.zeros(len(feature_columns))
    
    # Normalisation des valeurs numériques
    numeric_array = np.array([[rate, year, runtime, budget]])
    normalized_values = scaler.transform(numeric_array)
    
    # Attribution des valeurs normalisées
    for i, feature in enumerate(numeric_features):
        input_features[feature_columns.index(feature)] = normalized_values[0][i]
    
    # Attribution du genre sélectionné
    if selected_genre in genre_columns:
        genre_idx = feature_columns.index(selected_genre)
        input_features[genre_idx] = 1
    
    # Recherche des films similaires
    distances, indices = model.kneighbors([input_features])
    
    return df.iloc[indices[0]]
