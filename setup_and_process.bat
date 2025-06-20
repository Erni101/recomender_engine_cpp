@echo off
echo Creando entorno virtual...
python -m venv venv
call venv\Scripts\activate

echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

echo Procesando datos de Amazon...
python process_amazon_data.py

echo Proceso completado. Los archivos generados estan en la carpeta 'models'.
pause
