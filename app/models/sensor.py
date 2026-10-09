from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Sensor(Base):
    __tablename__ = "sensores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str | None] = mapped_column(String(100))
    categoria: Mapped[str | None] = mapped_column(String(30))
    ubicacion: Mapped[str | None] = mapped_column(String(100))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_registro: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))

    sensor_magnitudes = relationship(
        "SensorMagnitud",
        back_populates="sensor",
    )