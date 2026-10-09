from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.sensor_magnitudes import obtener_sensor_magnitud_por_id
from app.database.dependencies import obtener_db
from app.schemas.sensor_magnitud import SensorMagnitudRespuesta


router = APIRouter(
    prefix="/sensor-magnitudes",
    tags=["Sensor-Magnitudes"],
)


@router.get("/{sensor_magnitud_id}", response_model=SensorMagnitudRespuesta)
def obtener_sensor_magnitud(
    sensor_magnitud_id: int,
    db: Session = Depends(obtener_db),
):
    sensor_magnitud = obtener_sensor_magnitud_por_id(
        db,
        sensor_magnitud_id,
    )

    if sensor_magnitud is None:
        raise HTTPException(
            status_code=404,
            detail="La relación sensor-magnitud no existe",
        )

    return sensor_magnitud