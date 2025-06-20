import os
import json
import gzip
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from collections import defaultdict
import struct

def load_magazine_data(file_path):
    """Carga los datos de las revistas desde el archivo JSON."""
    reviews = []
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        for line in f:
            try:
                review = json.loads(line)
                # Asegurarse de que la reseña tenga los campos necesarios
                if 'reviewerID' in review and 'asin' in review and 'overall' in review:
                    reviews.append({
                        'user_id': review['reviewerID'],
                        'item_id': review['asin'],
                        'rating': float(review['overall']),
                        'text': review.get('reviewText', '') + ' ' + review.get('summary', '')
                    })
            except json.JSONDecodeError as e:
                print(f"Error al decodificar línea: {e}")
    return pd.DataFrame(reviews)

def preprocess_data(df):
    """Preprocesa los datos para el modelo."""
    # Filtrar usuarios e ítems con suficientes interacciones
    min_user_ratings = 3
    min_item_ratings = 3
    
    user_counts = df['user_id'].value_counts()
    item_counts = df['item_id'].value_counts()
    
    filtered_df = df[
        (df['user_id'].isin(user_counts[user_counts >= min_user_ratings].index)) & 
        (df['item_id'].isin(item_counts[item_counts >= min_item_ratings].index))
    ]
    
    return filtered_df

def create_interaction_matrix(df):
    """Crea una matriz de interacciones usuario-ítem."""
    # Crear matriz de interacciones
    interactions = df.pivot_table(
        index='user_id', 
        columns='item_id', 
        values='rating', 
        fill_value=0
    )
    
    # Normalizar las calificaciones
    user_means = interactions.mean(axis=1)
    interactions = interactions.sub(user_means, axis=0)
    
    return interactions, user_means

def generate_embeddings(interactions, n_components=50):
    """Genera embeddings de usuarios e ítems usando SVD."""
    # Aplicar SVD a la matriz de interacciones
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    item_embeddings = svd.fit_transform(interactions.T)
    
    # Calcular embeddings de usuarios
    user_embeddings = interactions.values @ item_embeddings @ np.linalg.pinv(np.diag(svd.singular_values_[:n_components]))
    
    # Normalizar los embeddings
    item_embeddings = item_embeddings / np.linalg.norm(item_embeddings, axis=1, keepdims=True)
    user_embeddings = user_embeddings / np.linalg.norm(user_embeddings, axis=1, keepdims=True)
    
    return user_embeddings, item_embeddings, interactions.columns, interactions.index

def save_embeddings(embeddings, ids, path):
    """Guarda los embeddings en un archivo binario."""
    with open(path, 'wb') as f:
        # Número de elementos y dimensión
        num_items = len(ids)
        dim = embeddings.shape[1] if num_items > 0 else 0
        
        # Escribir encabezado
        f.write(struct.pack('I', num_items))  # Número de elementos
        f.write(struct.pack('I', dim))        # Dimensión de los embeddings
        
        # Escribir IDs
        for item_id in ids:
            item_id_bytes = str(item_id).encode('utf-8')
            f.write(struct.pack('I', len(item_id_bytes)))  # Longitud del ID
            f.write(item_id_bytes)                         # Bytes del ID
        
        # Escribir embeddings
        f.write(embeddings.astype(np.float32).tobytes())

def save_ids(ids, path):
    """Guarda los IDs en un archivo de texto."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(str(id) for id in ids))

def main():
    # Rutas de archivos
    data_dir = 'data'
    models_dir = 'models'
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    # Cargar datos
    print("Cargando datos de revistas...")
    df = load_magazine_data(os.path.join(data_dir, 'Magazine_Subscriptions_5.json.gz'))
    print(f"Se cargaron {len(df)} reseñas de {df['user_id'].nunique()} usuarios y {df['item_id'].nunique()} revistas.")
    
    # Preprocesar datos
    print("\nPreprocesando datos...")
    df = preprocess_data(df)
    print(f"Después del filtrado: {len(df)} reseñas de {df['user_id'].nunique()} usuarios y {df['item_id'].nunique()} revistas.")
    
    # Crear matriz de interacciones
    print("\nCreando matriz de interacciones...")
    interactions, user_means = create_interaction_matrix(df)
    
    # Generar embeddings
    print("\nGenerando embeddings...")
    user_embeddings, item_embeddings, item_ids, user_ids = generate_embeddings(interactions)
    
    # Guardar embeddings
    print("\nGuardando modelos...")
    save_embeddings(user_embeddings, user_ids, os.path.join(models_dir, 'user_embeddings.bin'))
    save_embeddings(item_embeddings, item_ids, os.path.join(models_dir, 'item_embeddings.bin'))
    
    # Guardar IDs
    save_ids(user_ids, os.path.join(data_dir, 'users.txt'))
    save_ids(item_ids, os.path.join(data_dir, 'items.txt'))
    
    print("\n¡Proceso completado!")
    print(f"- Usuarios: {len(user_ids)}")
    print(f"- Revistas: {len(item_ids)}")
    print(f"- Dimensión de los embeddings: {item_embeddings.shape[1]}")

if __name__ == "__main__":
    main()
