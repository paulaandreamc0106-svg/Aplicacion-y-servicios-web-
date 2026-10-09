from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sensor_magnitud import SensorMagnitud


def obtener_sensor_magnitud(
    db: Session,
    sensor_id: int,
    magnitud: str,
) -> SensorMagnitud | None:
    consulta = select(SensorMagnitud).where(
        SensorMagnitud.sensor_id == sensor_id,
        SensorMagnitud.magnitud == magnitud,
    )

    return db.execute(consulta).scalar_one_or_none()


def obtener_magnitudes_por_sensor(
    db: Session,
    sensor_id: int,
) -> list[SensorMagnitud]:
    consulta = select(SensorMagnitud).where(
        SensorMagnitud.sensor_id == sensor_id
    ).order_by(SensorMagnitud.id)

    return list(db.execute(consulta).scalars().all())


def obtener_sensor_magnitud_por_id(
    db: Session,
    sensor_magnitud_id: int,
) -> SensorMagnitud | None:
    consulta = select(SensorMagnitud).where(
        SensorMagnitud.id == sensor_magnitud_id
    )

    return db.execute(consulta).scalar_one_or_none()