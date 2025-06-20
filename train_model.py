import json
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from implicit.als import AlternatingLeastSquares
from implicit.nearest_neighbours import bm25_weight
import os

def load_data(filepath):
    """Carga los datos del archivo JSON"""
    reviews = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            reviews.append(json.loads(line))
    return pd.DataFrame(reviews)

def prepare_data(df):
    """Prepara los datos para el modelo"""
    # Filtrar solo las columnas necesarias
    df = df[['reviewerID', 'asin', 'overall']].copy()
    
    # Crear índices numéricos para usuarios e ítems
    df['user_idx'] = df['reviewerID'].astype('category').cat.codes
    df['item_idx'] = df['asin'].astype('category').cat.codes
    
    # Mapeo de índices a IDs originales
    user_mapping = dict(enumerate(df['reviewerID'].astype('category').cat.categories))
    item_mapping = dict(enumerate(df['asin'].astype('category').cat.categories))
    
    # Crear matriz usuario-ítem
    ratings = csr_matrix((df['overall'], (df['user_idx'], df['item_idx'])))
    
    return ratings, user_mapping, item_mapping

def train_model(ratings, factors=50, iterations=15):
    """Entrena el modelo ALS"""
    # Ponderar las calificaciones con BM25
    ratings = bm25_weight(ratings, K1=100, B=0.8)
    
    # Crear y entrenar el modelo
    model = AlternatingLeastSquares(
        factors=factors,
        iterations=iterations,
        calculate_training_loss=True,
        random_state=42
    )
    
    model.fit(ratings)
    return model

def save_embeddings(model, user_mapping, item_mapping, output_dir='models'):
    """Guarda los embeddings en formato binario"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Guardar embeddings de usuarios
    with open(os.path.join(output_dir, 'user_embeddings.bin'), 'wb') as f:
        # Número de usuarios y dimensión
        num_users = len(user_mapping)
        dim = model.user_factors.shape[1]
        f.write(np.int32(num_users).tobytes())
        f.write(np.int32(dim).tobytes())
        
        # Guardar mapeo de usuarios
        for idx in range(num_users):
            user_id = user_mapping[idx].encode('utf-8')
            f.write(np.int32(len(user_id)).tobytes())
            f.write(user_id)
        
        # Guardar embeddings
        model.user_factors.astype(np.float32).tofile(f)
    
    # Guardar embeddings de ítems
    with open(os.path.join(output_dir, 'item_embeddings.bin'), 'wb') as f:
        # Número de ítems y dimensión
        num_items = len(item_mapping)
        dim = model.item_factors.shape[1]
        f.write(np.int32(num_items).tobytes())
        f.write(np.int32(dim).tobytes())
        
        # Guardar mapeo de ítems
        for idx in range(num_items):
            item_id = item_mapping[idx].encode('utf-8')
            f.write(np.int32(len(item_id)).tobytes())
            f.write(item_id)
        
        # Guardar embeddings
        model.item_factors.astype(np.float32).tofile(f)

def main():
    # Rutas de los archivos
    data_path = os.path.join('data', 'Magazine_Subscriptions_5.json', 'Magazine_Subscriptions_5.json')
    
    print("Cargando datos...")
    df = load_data(data_path)
    
    print("Preparando datos...")
    ratings, user_mapping, item_mapping = prepare_data(df)
    
    print(f"Entrenando modelo con {len(user_mapping)} usuarios y {len(item_mapping)} ítems...")
    model = train_model(ratings)
    
    print("Guardando embeddings...")
    save_embeddings(model, user_mapping, item_mapping)
    
    print("¡Entrenamiento completado!")
    print(f"Embeddings guardados en la carpeta 'models'")

if __name__ == "__main__":
    main()
