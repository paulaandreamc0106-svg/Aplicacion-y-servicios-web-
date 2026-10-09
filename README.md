# Guía de Trabajo Práctico Experimental — Taller 2
**API para adquisición, validación y consulta de datos IoT con FastAPI, MQTT y PostgreSQL**

---

## 1. Información General
* **Integrantes:** Paula Andrea Montoya Corrales y Juan Esteban Velez Tobon 
* **Asignatura:** Aplicaciones y Servicios Web
* **Programa Académico:** Tecnología en Desarrollo de Software (ITM)
* **Fecha:** 8 de Octubre de 2026
* **Sensor Asignado:** `AQ-002` (ID en BD: 2)
* **Tópico MQTT Utilizado:** `iot/sensors/AQ-002/data`

---

## 2. Descripción del Sistema
El sistema permite capturar, validar, almacenar y consultar datos telemétricos emitidos por sensores IoT en tiempo real. 

### Arquitectura
1. **Consumidor MQTT:** Escucha continuamente el tópico asignado mediante un cliente `paho-mqtt` ejecutado en segundo plano en el ciclo de vida de FastAPI (`lifespan`).
2. **Validación:** Comprueba la estructura con **Pydantic** y las reglas de negocio (rangos, unidades, estados del sensor) mediante **SQLAlchemy ORM**.
3. **Persistencia:** Guarda los mensajes válidos en la base de datos PostgreSQL.
4. **API REST:** Expone endpoints con **FastAPI** para consultar el histórico, la última medición y la información del sensor, retornando fechas ajustadas a la zona horaria de Colombia (UTC-5).

---

## 3. Configuración del Entorno
```bash
# Activar entorno virtual
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor con recarga automática
python -m uvicorn app.main:app --reload

Variables requeridas en el archivo .env:
MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, MQTT_USERNAME, MQTT_PASSWORD, DATABASE_URL.

4. Organización del Código
app/models/: Definición de tablas ORM con SQLAlchemy (sensor.py, sensor_magnitud.py, medicion.py).

app/schemas/: Esquemas de validación y serialización con Pydantic (sensor.py, medicion.py, mqtt.py).

app/crud/: Funciones de acceso y manipulación de la base de datos (sensores.py, mediciones.py, validaciones.py).

app/api/: Rutas HTTP y controladores REST de FastAPI (sensores.py, mediciones.py).

app/mqtt/: Suscriptor y consumidor del broker MQTT (client.py).

app/database/: Configuración y conexión con PostgreSQL (connection.py).

## 5. Endpoints Implementados

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/sensores` | Lista todos los sensores registrados |
| `GET` | `/sensores/{id}` | Muestra los detalles de un sensor por su ID |
| `GET` | `/sensores/por-codigo/{codigo}` | Consulta un sensor por su código telemétrico |
| `GET` | `/sensores/{id}/magnitudes` | Lista las magnitudes asociadas a un sensor |
| `GET` | `/sensor-magnitudes/{id}` | Muestra la configuración de una magnitud |
| `GET` | `/mediciones/{id}` | Consulta una medición por su ID numérico |
| `GET` | `/sensores/{id}/mediciones` | Consulta datos históricos con filtros por fechas, magnitud y límite |
| `GET` | `/sensores/{id}/ultima-medicion` | Retorna la última medición registrada del sensor |

6. Evidencias de Funcionamiento
Las capturas correspondientes a las pruebas obligatorias se encuentran almacenadas en la carpeta /evidencias:

    1. Recepción MQTT: evidencias/01_recepcion_mqtt.png — Procesamiento de mensajes continuos durante más de 20 minutos.

    2. Consulta con éxito (200 OK): evidencias/02_consulta_mediciones_200.png — Datos históricos retornados correctamente.

    3. Sensor Inexistente (404 Not Found): evidencias/03_sensor_404.png — Intento de consulta a ID no registrado.

    4. Fechas inválidas (400 Bad Request): evidencias/04_rango_fechas_400.png — Validación al enviar desde > hasta.

    5. Formato incorrecto (422 Unprocessable Entity): evidencias/05_validacion_422.png — Esquema de validación para parámetros erróneos.

    6. Última Medición y Conversión Horaria: evidencias/06_ultima_medicion.png — Respuesta formateada en zona de Colombia (-05:00).

    7. Conclusiones
    
    1. Se logró integrar un flujo asíncrono consumidor de MQTT dentro del ciclo de vida de una API web con FastAPI.

    2. La separación de capas (schemas, models, crud, api) facilita la escalabilidad y el mantenimiento del software.

    3. Se garantizó la integridad de la base de datos al filtrar mensajes fuera de rango o con unidades inadecuadas antes de realizar los commits.