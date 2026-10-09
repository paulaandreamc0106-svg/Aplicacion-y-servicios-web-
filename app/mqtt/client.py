import json
import os

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from pydantic import ValidationError

import app.models

from app.crud.sensor_magnitudes import obtener_sensor_magnitud
from app.crud.sensores import obtener_sensor_por_codigo
from app.crud.validaciones import validar_medicion
from app.crud.mediciones import crear_mediciones
from app.database.connection import SessionLocal
from app.schemas.mqtt import MqttPayload

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", "60"))

cliente_mqtt = None


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado al broker MQTT.")
        print("Suscribiendo al tópico:", MQTT_TOPIC)
        client.subscribe(MQTT_TOPIC)
    else:
        print("Error al conectar. Código:", reason_code)


def on_message(client, userdata, message):
    db = SessionLocal()

    try:
        payload = json.loads(message.payload.decode("utf-8"))

        datos = MqttPayload.model_validate(payload)

        print("Mensaje MQTT recibido y validado.")

        sensor = obtener_sensor_por_codigo(
            db,
            datos.sensor_id,
        )

        if sensor is None:
            print("Mensaje rechazado: el sensor no existe.")
            return

        if not sensor.activo:
            print("Mensaje rechazado: el sensor está inactivo.")
            return

        mediciones_para_guardar = []

        for magnitud, medicion in datos.measurements.items():

            es_valida, mensaje = validar_medicion(
                db,
                datos.sensor_id,
                magnitud,
                medicion.value,
                medicion.unit,
            )

            if not es_valida:
                print(
                    f"Mensaje rechazado. "
                    f"Magnitud: {magnitud}. "
                    f"Motivo: {mensaje}"
                )
                return

            sensor_magnitud = obtener_sensor_magnitud(
                db,
                sensor.id,
                magnitud,
            )

            mediciones_para_guardar.append(
                {
                    "sensor_magnitud_id": sensor_magnitud.id,
                    "valor": medicion.value,
                    "timestamp_utc": datos.timestamp,
                }
            )

        crear_mediciones(
            db,
            mediciones_para_guardar,
        )

        print(
            f"Mensaje almacenado correctamente. "
            f"Mediciones guardadas: {len(mediciones_para_guardar)}"
        )

    except json.JSONDecodeError:
        print("Mensaje rechazado: JSON inválido.")

    except ValidationError as error:
        print("Mensaje rechazado por validación Pydantic:")
        print(error)

    except Exception as error:
        db.rollback()
        print("Error procesando mensaje MQTT:")
        print(error)

    finally:
        db.close()


def iniciar_mqtt():
    global cliente_mqtt
    cliente_mqtt = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2
    )

    if MQTT_USERNAME and MQTT_PASSWORD:
        cliente_mqtt.username_pw_set(
            MQTT_USERNAME,
            MQTT_PASSWORD,
        )

    cliente_mqtt.on_connect = on_connect
    cliente_mqtt.on_message = on_message

    cliente_mqtt.connect(
        MQTT_BROKER,
        MQTT_PORT,
        MQTT_KEEPALIVE,
    )
    cliente_mqtt.loop_start()


def detener_mqtt():
    global cliente_mqtt
    if cliente_mqtt:
        cliente_mqtt.loop_stop()
        cliente_mqtt.disconnect()