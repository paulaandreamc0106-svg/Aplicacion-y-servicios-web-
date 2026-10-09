from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.medicion import Medicion
from app.models.sensor_magnitud import SensorMagnitud


def crear_mediciones(
    db: Session,
    mediciones: list[dict],
) -> list[Medicion]:
    fecha_recepcion = datetime.now(timezone.utc)

    objetos = []

    for datos in mediciones:
        medicion = Medicion(
            sensor_magnitud_id=datos["sensor_magnitud_id"],
            valor=datos["valor"],
            timestamp_utc=datos["timestamp_utc"],
            fecha_recepcion=fecha_recepcion,
        )

        db.add(medicion)
        objetos.append(medicion)

    db.commit()

    for medicion in objetos:
        db.refresh(medicion)

    return objetos


def obtener_medicion_por_id(
    db: Session,
    medicion_id: int,
) -> Medicion | None:
    consulta = select(Medicion).where(
        Medicion.id == medicion_id
    )

    return db.execute(consulta).scalar_one_or_none()


def obtener_mediciones_por_sensor(
    db: Session,
    sensor_id: int,
    desde: datetime | None = None,
    hasta: datetime | None = None,
    magnitud: str | None = None,
    limit: int = 100,
) -> list[Medicion]:
    consulta = (
        select(Medicion)
        .join(Medicion.sensor_magnitud)
        .where(
            SensorMagnitud.sensor_id == sensor_id
        )
    )

    if desde is not None:
        consulta = consulta.where(Medicion.timestamp_utc >= desde)

    if hasta is not None:
        consulta = consulta.where(Medicion.timestamp_utc <= hasta)

    if magnitud is not None:
        consulta = consulta.where(SensorMagnitud.magnitud == magnitud)

    consulta = consulta.order_by(
        Medicion.timestamp_utc.desc(),
        Medicion.id.desc(),
    ).limit(limit)

    return list(
        db.execute(consulta).scalars().all()
    )


def obtener_ultima_medicion_por_sensor(
    db: Session,
    sensor_id: int,
) -> Medicion | None:
    consulta = (
        select(Medicion)
        .join(Medicion.sensor_magnitud)
        .where(SensorMagnitud.sensor_id == sensor_id)
        .order_by(
            Medicion.timestamp_utc.desc(),
            Medicion.id.desc(),
        )
        .limit(1)
    )

    return db.execute(consulta).scalar_one_or_none()