import os
import shutil
import sys
import json

def copy_files():
    # Crear directorio build si no existe
    os.makedirs('build', exist_ok=True)
    
    # Copiar archivos necesarios
    files_to_copy = [
        ('models/user_embeddings.bin', 'build/'),
        ('models/item_embeddings.bin', 'build/'),
        ('data/users.txt', 'build/'),
        ('data/items.txt', 'build/')
    ]
    
    for src, dst in files_to_copy:
        try:
            shutil.copy2(src, dst)
            print(f"Copiado: {src} -> {dst}")
        except Exception as e:
            print(f"Error al copiar {src}: {e}")
    
    # Crear archivo de configuración personalizado para la carpeta build
    config = {
        "model_paths": {
            "user_embeddings": "user_embeddings.bin",
            "item_embeddings": "item_embeddings.bin"
        },
        "data_paths": {
            "users": "users.txt",
            "items": "items.txt"
        },
        "recommendation": {
            "top_k": 10,
            "similarity_threshold": 0.7,
            "embedding_dim": 64
        },
        "training": {
            "factors": 64,
            "regularization": 0.01,
            "iterations": 20
        }
    }
    
    # Guardar configuración en la carpeta build
    config_path = os.path.join('build', 'config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Creado archivo de configuración en: {config_path}")

if __name__ == "__main__":
    print("Preparando archivos para el motor de recomendaciones...")
    copy_files()
    print("\nAhora puedes ejecutar el servidor web con:")
    print("python web/app.py")
