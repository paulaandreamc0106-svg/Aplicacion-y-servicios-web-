from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SensorMagnitudRespuesta(BaseModel):
    id: int
    sensor_id: int
    magnitud: str
    unidad: str
    valor_minimo: Decimal | None
    valor_maximo: Decimal | None

    model_config = ConfigDict(from_attributes=True)