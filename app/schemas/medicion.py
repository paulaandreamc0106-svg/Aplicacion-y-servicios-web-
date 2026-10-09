from datetime import datetime, timezone, timedelta
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_serializer


COLOMBIA_TZ = timezone(timedelta(hours=-5))


class MedicionRespuesta(BaseModel):
    id: int
    sensor_magnitud_id: int
    valor: Decimal
    timestamp_utc: datetime
    fecha_recepcion: datetime | None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("timestamp_utc", "fecha_recepcion")
    def serializar_fecha_colombia(self, dt: datetime | None) -> str | None:
        if dt is None:
            return None
        fecha_colombia = dt.astimezone(COLOMBIA_TZ)
        return fecha_colombia.isoformat()