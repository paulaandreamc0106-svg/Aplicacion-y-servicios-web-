from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.sensor import Sensor


def obtener_sensor_por_codigo(db: Session, codigo: str) -> Sensor | None:
    consulta = select(Sensor).where(Sensor.codigo == codigo)
    return db.execute(consulta).scalar_one_or_none()


def obtener_sensores(db: Session) -> list[Sensor]:
    consulta = select(Sensor).order_by(Sensor.id)
    return list(db.execute(consulta).scalars().all())


def obtener_sensor_por_id(db: Session, sensor_id: int) -> Sensor | None:
    consulta = select(Sensor).where(Sensor.id == sensor_id)
    return db.execute(consulta).scalar_one_or_none()