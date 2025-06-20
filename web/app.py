import os
import json
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Ruta al ejecutable de tu motor de recomendaciones
import sys
import pathlib

# Obtener la ruta base del proyecto
BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()

# Construir la ruta al ejecutable
if sys.platform == 'win32':
    # Para Windows
    RECOMMENDER_EXECUTABLE = str(BASE_DIR / 'build' / 'recommender_engine_cpp.exe')
else:
    # Para Unix/Linux/MacOS
    RECOMMENDER_EXECUTABLE = str(BASE_DIR / 'build' / 'recommender_engine_cpp')

# Verificar que el archivo existe
if not os.path.exists(RECOMMENDER_EXECUTABLE):
    print(f"ADVERTENCIA: No se encontró el ejecutable en {RECOMMENDER_EXECUTABLE}")
    print("Asegúrate de haber compilado el proyecto con CMake.")
else:
    print(f"Ejecutable encontrado en: {RECOMMENDER_EXECUTABLE}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'Se requiere un ID de usuario'}), 400
        
        # Verificar que el ejecutable existe
        if not os.path.exists(RECOMMENDER_EXECUTABLE):
            return jsonify({
                'error': 'Motor de recomendaciones no encontrado',
                'path': RECOMMENDER_EXECUTABLE
            }), 500
            
        print(f"Ejecutando: {RECOMMENDER_EXECUTABLE} {user_id}")
        
        # Ejecutar el motor de recomendaciones
        try:
            result = subprocess.run(
                [RECOMMENDER_EXECUTABLE, user_id],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(RECOMMENDER_EXECUTABLE)  # Ejecutar desde el directorio del ejecutable
            )
            
            print(f"Salida estándar: {result.stdout}")
            print(f"Error estándar: {result.stderr}")
            print(f"Código de salida: {result.returncode}")
            
            if result.returncode != 0:
                return jsonify({
                    'error': 'Error al ejecutar el motor de recomendaciones',
                    'details': result.stderr,
                    'returncode': result.returncode
                }), 500
            
            # Procesar la salida
            if not result.stdout.strip():
                return jsonify({
                    'error': 'El motor no devolvió ningún resultado',
                    'user_id': user_id,
                    'recommendations': []
                })
                
            lines = result.stdout.strip().split('\n')
            print(f"Líneas de salida: {lines}")
            
            # Buscar recomendaciones (pueden comenzar con '-' o con otro formato)
            recommendations = []
            for line in lines:
                line = line.strip()
                if line.startswith('- '):
                    recommendations.append(line[2:].strip())
                elif line and not line.startswith('Recommendations for user'):
                    recommendations.append(line)
            
            print(f"Recomendaciones procesadas: {recommendations}")
            
            return jsonify({
                'user_id': user_id,
                'recommendations': recommendations
            })
            
        except subprocess.CalledProcessError as e:
            return jsonify({
                'error': 'Error al ejecutar el motor',
                'details': str(e),
                'output': e.output,
                'stderr': e.stderr if hasattr(e, 'stderr') else ''
            }), 500
        
    except Exception as e:
        import traceback
        return jsonify({
            'error': 'Error interno del servidor',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
