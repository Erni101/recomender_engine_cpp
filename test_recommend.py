import os
import subprocess
import sys
import pathlib

# Obtener la ruta base del proyecto
BASE_DIR = pathlib.Path(__file__).parent.absolute()

# Construir la ruta al ejecutable
if sys.platform == 'win32':
    # Para Windows
    RECOMMENDER_EXECUTABLE = str(BASE_DIR / 'build' / 'recommender_engine_cpp.exe')
else:
    # Para Unix/Linux/MacOS
    RECOMMENDER_EXECUTABLE = str(BASE_DIR / 'build' / 'recommender_engine_cpp')

# Verificar que el archivo existe
if not os.path.exists(RECOMMENDER_EXECUTABLE):
    print(f"ERROR: No se encontró el ejecutable en {RECOMMENDER_EXECUTABLE}")
    print("Asegúrate de haber compilado el proyecto con CMake.")
    sys.exit(1)

print(f"Ejecutable encontrado en: {RECOMMENDER_EXECUTABLE}")

# Probar con un usuario de prueba
user_id = "user_1"
print(f"\nProbando con usuario: {user_id}")

try:
    result = subprocess.run(
        [RECOMMENDER_EXECUTABLE, user_id],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(RECOMMENDER_EXECUTABLE)
    )
    
    print("\n=== RESULTADO ===")
    print(f"Código de salida: {result.returncode}")
    print("\nSalida estándar:")
    print(result.stdout)
    print("\nError estándar:")
    print(result.stderr)
    
except Exception as e:
    print(f"\nERROR al ejecutar el comando: {e}")
    import traceback
    traceback.print_exc()
