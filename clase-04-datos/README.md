Clase 4 — Manejo de datos e interacción entre aplicaciones

En esta práctica se trabaja con un archivo CSV que contiene información de estudiantes. Los datos son procesados y modificados mediante Python para finalmente crear un archivo en formato JSON.

Proceso
estudiantes.csv → Python → procesamiento de datos → estudiantes_resumen.json

Tecnologías empleadas
Python 3
Módulo csv
Módulo json
Librería pathlib
Ejecución
Para poner en funcionamiento el programa, se debe ejecutar el siguiente comando:

python transformar_estudiantes.py

El programa obtiene los datos de los estudiantes desde el archivo CSV, realiza la transformación de cada registro y crea el archivo JSON correspondiente. Después, el archivo JSON es deserializado para presentar en pantalla los datos del primer estudiante y la cantidad total de registros procesados.