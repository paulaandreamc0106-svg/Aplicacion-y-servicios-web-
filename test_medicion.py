from datetime import datetime, timezone

from app.crud.mediciones import crear_medicion
from app.database.connection import SessionLocal

# Cargar los modelos de SQLAlchemy
from app.models.sensor import Sensor
from app.models.sensor_magnitud import SensorMagnitud
from app.models.medicion import Medicion


db = SessionLocal()

try:
    medicion = crear_medicion(
        db=db,
        sensor_magnitud_id=4,
        valor=25.4,
        timestamp_utc=datetime(
            2026,
            10,
            8,
            4,
            0,
            0,
            tzinfo=timezone.utc,
        ),
    )

    print("Medición creada correctamente")
    print("ID:", medicion.id)
    print("Sensor-magnitud ID:", medicion.sensor_magnitud_id)
    print("Valor:", medicion.valor)
    print("Timestamp UTC:", medicion.timestamp_utc)
    print("Fecha de recepción:", medicion.fecha_recepcion)

finally:
    db.close()