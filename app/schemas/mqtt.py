from datetime import datetime

from pydantic import BaseModel


class MeasurementData(BaseModel):
    value: float
    unit: str


class MqttPayload(BaseModel):
    sensor_id: str
    timestamp: datetime
    measurements: dict[str, MeasurementData]