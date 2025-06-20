# 🚀 Motor de Recomendaciones en C++

Un motor de recomendaciones de alto rendimiento implementado en C++ que utiliza embeddings para generar recomendaciones personalizadas basadas en similitud coseno.

## 🛠️ Requisitos

- Compilador C++17 o superior (GCC/Clang/MSVC)
- CMake 3.10 o superior
- Python 3.7+ (solo para generación de datos de prueba)
- Bibliotecas:
  - nlohmann/json (incluida en el código fuente)

## 🚀 Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/recomender_engine_cpp.git
   cd recomender_engine_cpp
   ```

2. Configurar el proyecto con CMake:
   ```bash
   mkdir -p build && cd build
   cmake ..
   ```

3. Compilar el proyecto:
   ```bash
   cmake --build .
   ```

## 🏗️ Estructura del Proyecto

```
recomender_engine_cpp/
├── include/                    # Archivos de cabecera
│   ├── recommender.hpp        # Clase principal del recomendador
│   ├── loader.hpp             # Utilidades para carga de datos
│   └── utils.hpp              # Utilidades matemáticas
├── src/                       # Código fuente
│   ├── main.cpp              # Punto de entrada
│   ├── recommender.cpp       # Implementación del recomendador
│   ├── loader.cpp            # Implementación de carga de datos
│   └── utils.cpp             # Implementación de utilidades
├── data/                      # Datos de ejemplo
├── models/                    # Modelos pre-entrenados
├── tests/                     # Pruebas unitarias
├── CMakeLists.txt            # Configuración de CMake
└── config.json               # Archivo de configuración
```

## 🚀 Uso

1. Ejecutar el programa con un ID de usuario:
   ```bash
   ./recommender_engine_cpp <user_id>
   ```

2. El programa mostrará las recomendaciones para el usuario especificado.

## 🧠 Procesamiento de Datos

### Datos de Amazon

El proyecto incluye un conjunto de datos de reseñas de revistas de Amazon. Para procesar estos datos y generar los embeddings necesarios:

1. Asegúrate de tener instaladas las dependencias de Python:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta el script de procesamiento:
   ```bash
   python process_amazon_data.py
   ```

Este script:
- Procesa el archivo `data/Magazine_Subscriptions_5.json.gz`
- Entrena un modelo de factorización de matrices (ALS)
- Genera los archivos de embeddings en la carpeta `models/`
- Crea listas de usuarios e ítems en `data/`

### Datos de Prueba

Para generar un conjunto de datos de prueba más pequeño, puedes usar:

```bash
python generate_test_data.py
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## 📧 Contacto

Tu Nombre - [@tu_twitter](https://twitter.com/tu_twitter) - tu@email.com

Enlace del proyecto: [https://github.com/tu-usuario/recomender_engine_cpp](https://github.com/tu-usuario/recomender_engine_cpp)
│   └── utils.hpp              # Funciones de utilidad
│
├── src/                       # Código fuente
│   ├── main.cpp               # Punto de entrada principal
│   ├── recommender.cpp        # Implementación del recomendador
│   ├── loader.cpp             # Implementación de carga de datos
│   └── utils.cpp              # Implementación de utilidades
│
├── models/                    # Archivos de modelo
│   ├── user_embeddings.bin    # Embeddings de usuarios
│   └── item_embeddings.bin    # Embeddings de ítems
│
├── data/                      # Datos de entrada
│   ├── users.txt              # Datos de usuarios
│   └── items.txt              # Datos de ítems
│
├── tests/                     # Pruebas unitarias
│   └── test_recommender.cpp   # Pruebas con Google Test
│
├── build/                     # Directorio de compilación
├── CMakeLists.txt             # Configuración de CMake
├── config.json                # Archivo de configuración
└── generate_test_data.py      # Script para generar datos de prueba
```

## Requisitos

- CMake 3.10 o superior
- Compilador C++17 compatible (g++ 7+, clang 5+, MSVC 2017+)
- Python 3.6+ (solo para generar datos de prueba)
- Bibliotecas:
  - nlohmann/json (para manejo de JSON)
  - Google Test (para pruebas unitarias, opcional)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone [url-del-repositorio]
   cd recommender_engine_cpp
   ```

2. Instala las dependencias:
   ```bash
   # En Ubuntu/Debian
   sudo apt-get install build-essential cmake
   
   # O usando vcpkg
   vcpkg install nlohmann-json
   vcpkg install gtest
   ```

3. Genera datos de prueba (opcional):
   ```bash
   python generate_test_data.py
   ```

## Compilación

```bash
# Crea el directorio de compilación
mkdir build
cd build

# Configura con CMake
cmake ..

# O para configurar con vcpkg
# cmake .. -DCMAKE_TOOLCHAIN_FILE=[ruta-a-vcpkg]/scripts/buildsystems/vcpkg.cmake

# Compila el proyecto
cmake --build .
```

## Uso

1. Ejecuta el programa principal:
   ```bash
   ./recommender_engine_cpp user_0
   ```
   Esto generará recomendaciones para el usuario "user_0".

2. Para ejecutar las pruebas unitarias:
   ```bash
   ctest
   ```

## Configuración

El archivo `config.json` contiene la configuración del sistema:
- `model_paths`: Rutas a los archivos de embeddings
- `data_paths`: Rutas a los archivos de datos de texto
- `recommendation`: Configuración de recomendaciones (top-k, umbral de similitud)
- `system`: Configuración del sistema (nivel de log, tamaño de caché)

## Generación de Datos de Prueba

El script `generate_test_data.py` genera datos de prueba aleatorios:
- 100 usuarios con embeddings de 50 dimensiones
- 1000 ítems con embeddings de 50 dimensiones
- Archivos de texto con IDs de usuarios e ítems

Para generar los datos:
```bash
python generate_test_data.py
```

## Estructura del Código

- `recommender.hpp/cpp`: Clase principal que maneja las recomendaciones
- `loader.hpp/cpp`: Utilidades para cargar y guardar embeddings
- `utils.hpp/cpp`: Funciones de utilidad (cálculo de similitud, etc.)
- `main.cpp`: Punto de entrada del programa

## Pruebas

Las pruebas unitarias utilizan Google Test. Para compilar y ejecutar las pruebas:

```bash
mkdir -p build
cd build
cmake .. -DBUILD_TESTS=ON
make
ctest --output-on-failure
```

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
