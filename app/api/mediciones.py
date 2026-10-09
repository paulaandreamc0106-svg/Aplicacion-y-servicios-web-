from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.mediciones import obtener_medicion_por_id
from app.database.dependencies import obtener_db
from app.schemas.medicion import MedicionRespuesta


router = APIRouter(
    prefix="/mediciones",
    tags=["Mediciones"],
)


@router.get("/{medicion_id}", response_model=MedicionRespuesta)
def obtener_medicion(
    medicion_id: int,
    db: Session = Depends(obtener_db),
):
    medicion = obtener_medicion_por_id(
        db,
        medicion_id,
    )

    if medicion is None:
        raise HTTPException(
            status_code=404,
            detail="La medición no existe",
        )

    return medicion