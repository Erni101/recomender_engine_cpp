# 🚀 Motor de Recomendaciones en C++ con Interfaz Web

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![C++17](https://img.shields.io/badge/C++-17-blue.svg)](https://en.cppreference.com/)
[![CMake](https://img.shields.io/badge/CMake-3.10+-064F8C.svg?logo=cmake)](https://cmake.org/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)

Un motor de recomendaciones de alto rendimiento implementado en C++ con una interfaz web en Python/Flask. Este proyecto procesa datos de reseñas de revistas de Amazon para proporcionar recomendaciones personalizadas de manera eficiente.

## ✨ Características

- 🚀 **Motor C++** - Alto rendimiento y eficiencia
- 🐍 **Python/Flask** - Interfaz web moderna y responsiva
- 🔧 **CMake** - Sistema de compilación multiplataforma
- 🔍 **Algoritmos Avanzados** - Búsqueda por similitud coseno
- 📊 **Procesamiento de Datos** - Escalable y eficiente
- 🎯 **Precisión** - Recomendaciones personalizadas basadas en comportamiento
- 🛠️ **Fácil Despliegue** - Configuración sencilla y documentación completa
- 📱 **Responsive** - Funciona en cualquier dispositivo

## 🏗️ Estructura del Proyecto

```
recomender_engine_cpp/
├── build/                     # Archivos de compilación (no versionado)
├── data/                      # Datos de entrada
│   ├── Magazine_Subscriptions_5.json.gz  # Dataset de Amazon
│   ├── users.txt              # Lista de usuarios
│   └── items.txt              # Lista de ítems
├── models/                    # Modelos generados (no versionado)
│   ├── user_embeddings.bin    # Embeddings de usuarios
│   └── item_embeddings.bin    # Embeddings de ítems
├── web/                       # Interfaz web
│   ├── static/               # Archivos estáticos (CSS, JS)
│   └── templates/            # Plantillas HTML
│       └── index.html        # Página principal
├── CMakeLists.txt            # Configuración de CMake
├── config.json               # Configuración de la aplicación
├── process_magazine_data.py  # Procesa datos de Amazon
├── prepare_build.py          # Prepara el entorno de compilación
├── requirements.txt          # Dependencias de Python
├── README.md                # Este archivo
└── LICENSE                  # Licencia MIT
```

## 🚀 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tuusuario/recomender_engine_cpp.git
   cd recomender_engine_cpp
   ```

2. **Configurar entorno virtual de Python**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Procesar los datos**
   ```bash
   python process_magazine_data.py
   ```

4. **Compilar el motor C++**
   ```bash
   mkdir -p build && cd build
   cmake ..
   cmake --build .
   cd ..
   ```

5. **Preparar archivos para el motor**
   ```bash
   python prepare_build.py
   ```

## 🖥️ Uso

1. **Iniciar el servidor web**
   ```bash
   python web/app.py
   ```

2. **Abrir en el navegador**
   ```
   http://localhost:5000
   ```

3. **Probar con usuarios de ejemplo**
   - Los IDs de usuario se pueden encontrar en `data/users.txt`
   - Ejemplo: `A10BWUA2MGA9BK`

## 📊 Datos

El proyecto utiliza el conjunto de datos [Amazon Magazine Subscriptions](https://nijianmo.github.io/amazon/index.html) que contiene reseñas de revistas de Amazon.

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🛠️ Requisitos

### Para compilación
- **Sistemas operativos:** Windows, Linux, macOS
- **Compilador C++17** o superior:
  - GCC 7+
  - Clang 5+
  - MSVC 2017+
- **CMake** 3.10 o superior
- **Git** (para clonar el repositorio)

### Para procesamiento de datos (opcional)
- **Python** 3.7 o superior
- **Dependencias de Python** (instalación automática):
  ```bash
  pip install -r requirements.txt
  ```
  - numpy
  - pandas
  - scipy
  - implicit
  - tqdm

## 🚀 Instalación Rápida

### Clonar el repositorio
```bash
git clone https://github.com/Erni101/recomender_engine_cpp.git
cd recomender_engine_cpp
```

### Compilar el proyecto
```bash
# Crear directorio de compilación
mkdir -p build && cd build

# Configurar con CMake
cmake ..

# O para modo Release
# cmake .. -DCMAKE_BUILD_TYPE=Release

# Compilar
cmake --build .
```

### Instalar dependencias de Python (opcional, solo para procesamiento de datos)
```bash
pip install -r requirements.txt
```

## 💻 Uso

### 1. Procesamiento de Datos

#### Procesar datos de Amazon
```bash
# Instalar dependencias (si no se han instalado)
pip install -r requirements.txt

# Procesar datos
python scripts/process_amazon_data.py
```

Este script:
- Procesa el archivo `data/Magazine_Subscriptions_5.json.gz`
- Entrena un modelo ALS (Alternating Least Squares)
- Genera los archivos de embeddings en `models/`
- Crea listas de usuarios e ítems en `data/`

#### Generar datos de prueba (opcional)
```bash
python scripts/generate_test_data.py
```

### 2. Ejecutar el Motor de Recomendaciones

```bash
# Navegar al directorio de compilación
cd build

# Ejecutar con un ID de usuario
./recommender_engine_cpp <user_id>

# Ejemplo:
# ./recommender_engine_cpp A2VY1BLSFMJ2MN
```

### 3. Ejecutar Pruebas Unitarias

```bash
cd build
ctest --output-on-failure
```

## ⚙️ Configuración

El archivo `config.json` controla el comportamiento del sistema:

```json
{
    "model_paths": {
        "user_embeddings": "models/user_embeddings.bin",
        "item_embeddings": "models/item_embeddings.bin"
    },
    "data_paths": {
        "users": "data/users.txt",
        "items": "data/items.txt",
        "raw_data": "data/Magazine_Subscriptions_5.json.gz"
    },
    "recommendation": {
        "top_k": 10,                    // Número de recomendaciones a generar
        "similarity_threshold": 0.7     // Umbral mínimo de similitud (0.0 a 1.0)
    },
    "training": {
        "factors": 64,                  // Dimensión de los embeddings
        "regularization": 0.01,         // Término de regularización
        "iterations": 20                // Número de iteraciones de entrenamiento
    }
}
```

### Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `RECOMMENDER_DEBUG` | Nivel de depuración (0-3) | 1 |
| `OMP_NUM_THREADS` | Número de hilos para procesamiento paralelo | Núcleos disponibles |

## 🧪 Pruebas

El proyecto incluye pruebas unitarias para validar el funcionamiento del motor:

### Ejecutar todas las pruebas
```bash
cd build
ctest --output-on-failure
```

### Ejecutar pruebas específicas
```bash
cd build
./tests/recommender_tests  # Ajusta el nombre del ejecutable según tu configuración
```

### Cobertura de código (Linux/macOS)
```bash
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Debug -DBUILD_COVERAGE=ON
make
test/run_tests.sh
```

## 🤝 Contribución

¡Gracias por considerar contribuir a este proyecto! Sigue estos pasos para contribuir:

1. 🍴 Haz un fork del repositorio
2. 🌿 Crea una rama para tu característica:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. 💾 Guarda tus cambios con mensajes descriptivos:
   ```bash
   git commit -m "feat: Añadir nueva funcionalidad"
   ```
4. 📤 Sube tus cambios:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. 🔄 Abre un Pull Request

### Convenciones de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` Nueva característica
- `fix:` Corrección de errores
- `docs:` Cambios en la documentación
- `style:` Formato, punto y coma, etc. (sin cambios en el código)
- `refactor:` Cambios en el código que no corrigen errores ni añaden características
- `perf:` Cambios que mejoran el rendimiento
- `test:` Añadir o corregir pruebas
- `chore:` Cambios en el proceso de construcción o herramientas auxiliares

## 📚 Documentación Adicional

### Estructura del Código

- **`include/recommender.hpp`**: Interfaz principal del motor de recomendaciones
- **`src/recommender.cpp`**: Implementación del algoritmo de recomendación
- **`include/loader.hpp`, `src/loader.cpp`**: Utilidades para cargar/guardar embeddings
- **`include/utils.hpp`, `src/utils.cpp`**: Funciones de utilidad (similitud coseno, normalización, etc.)
- **`src/main.cpp`**: Punto de entrada de la aplicación

### Generación de Datos de Prueba

El script `scripts/generate_test_data.py` crea un conjunto de datos sintético:

```bash
python scripts/generate_test_data.py
```

**Características de los datos generados:**
- 100 usuarios con embeddings de 50 dimensiones
- 1,000 ítems con embeddings de 50 dimensiones
- Archivos de texto con IDs de usuarios e ítems

## 🛠️ Despliegue

### Requisitos del Sistema
- 4GB+ de RAM (dependiendo del tamaño del dataset)
- 1GB+ de espacio en disco para los embeddings

### Rendimiento
- Tiempo de inferencia: < 100ms por recomendación (depende del hardware)
- Uso de memoria: ~500MB para 10,000 usuarios/ítems

## 📝 Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).

## 📧 Contacto

- **Autor**: Ernesto
- **GitHub**: [Erni101](https://github.com/Erni101)
- **Email**: ejgramckovillares@gmail.com

---

<div align="center">
  <p>© 2025 Ernesto Gramcko Villares. Todos los derechos reservados.</p>
  <p>Distribuido bajo la Licencia MIT.</p>
</div>
