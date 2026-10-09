from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SensorRespuesta(BaseModel):
    id: int
    codigo: str
    nombre: str | None
    categoria: str | None
    ubicacion: str | None
    activo: bool
    fecha_registro: datetime | None

    model_config = ConfigDict(from_attributes=True)