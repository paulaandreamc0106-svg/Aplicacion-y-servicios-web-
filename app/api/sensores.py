from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud.mediciones import (
    obtener_mediciones_por_sensor,
    obtener_ultima_medicion_por_sensor,
)
from app.crud.sensor_magnitudes import obtener_magnitudes_por_sensor
from app.crud.sensores import (
    obtener_sensor_por_codigo,
    obtener_sensor_por_id,
    obtener_sensores,
)
from app.database.dependencies import obtener_db
from app.schemas.medicion import MedicionRespuesta
from app.schemas.sensor import SensorRespuesta
from app.schemas.sensor_magnitud import SensorMagnitudRespuesta


router = APIRouter(prefix="/sensores", tags=["Sensores"])


@router.get("", response_model=list[SensorRespuesta])
def listar_sensores(db: Session = Depends(obtener_db)):
    return obtener_sensores(db)


@router.get("/por-codigo/{codigo}", response_model=SensorRespuesta)
def obtener_sensor_por_codigo_endpoint(
    codigo: str,
    db: Session = Depends(obtener_db),
):
    sensor = obtener_sensor_por_codigo(db, codigo)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="El sensor no existe",
        )

    return sensor


@router.get(
    "/{sensor_id}/magnitudes",
    response_model=list[SensorMagnitudRespuesta],
)
def listar_magnitudes_sensor(
    sensor_id: int,
    db: Session = Depends(obtener_db),
):
    sensor = obtener_sensor_por_id(db, sensor_id)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="El sensor no existe",
        )

    return obtener_magnitudes_por_sensor(db, sensor_id)


@router.get(
    "/{sensor_id}/mediciones",
    response_model=list[MedicionRespuesta],
)
def listar_mediciones_sensor(
    sensor_id: int,
    desde: datetime | None = Query(None, description="Fecha y hora inicial (ISO 8601)"),
    hasta: datetime | None = Query(None, description="Fecha y hora final (ISO 8601)"),
    magnitud: str | None = Query(None, description="Filtrar por nombre de magnitud"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros a retornar"),
    db: Session = Depends(obtener_db),
):
    sensor = obtener_sensor_por_id(db, sensor_id)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="El sensor no existe",
        )

    if desde is not None and hasta is not None and desde > hasta:
        raise HTTPException(
            status_code=400,
            detail="La fecha 'desde' no puede ser posterior a la fecha 'hasta'",
        )

    return obtener_mediciones_por_sensor(
        db,
        sensor_id=sensor_id,
        desde=desde,
        hasta=hasta,
        magnitud=magnitud,
        limit=limit,
    )


@router.get(
    "/{sensor_id}/ultima-medicion",
    response_model=MedicionRespuesta,
)
def obtener_ultima_medicion_sensor(
    sensor_id: int,
    db: Session = Depends(obtener_db),
):
    sensor = obtener_sensor_por_id(db, sensor_id)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="El sensor no existe",
        )

    medicion = obtener_ultima_medicion_por_sensor(db, sensor_id)

    if medicion is None:
        raise HTTPException(
            status_code=404,
            detail="El sensor no tiene mediciones registradas",
        )

    return medicion


@router.get("/{sensor_id}", response_model=SensorRespuesta)
def obtener_sensor(sensor_id: int, db: Session = Depends(obtener_db)):
    sensor = obtener_sensor_por_id(db, sensor_id)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="El sensor no existe",
        )

    return sensor