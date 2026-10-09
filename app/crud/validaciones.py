from sqlalchemy.orm import Session

from app.crud.sensor_magnitudes import obtener_sensor_magnitud
from app.crud.sensores import obtener_sensor_por_codigo


def validar_medicion(
    db: Session,
    sensor_codigo: str,
    magnitud: str,
    valor: float,
    unidad: str,
):
    # 1. Buscar el sensor por su código
    sensor = obtener_sensor_por_codigo(db, sensor_codigo)

    if sensor is None:
        return False, "El sensor no existe"

    # 2. Verificar que el sensor esté activo
    if not sensor.activo:
        return False, "El sensor está inactivo"

    # 3. Buscar la magnitud asociada al sensor
    sensor_magnitud = obtener_sensor_magnitud(
        db,
        sensor.id,
        magnitud,
    )

    if sensor_magnitud is None:
        return False, "La magnitud no pertenece al sensor"

    # 4. Verificar la unidad
    if sensor_magnitud.unidad != unidad:
        return False, "La unidad no coincide"

    # 5. Verificar el rango
    if sensor_magnitud.valor_minimo is not None:
        if valor < float(sensor_magnitud.valor_minimo):
            return False, "El valor está por debajo del mínimo permitido"

    if sensor_magnitud.valor_maximo is not None:
        if valor > float(sensor_magnitud.valor_maximo):
            return False, "El valor está por encima del máximo permitido"

    return True, "Medición válida"