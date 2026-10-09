from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class SensorMagnitud(Base):
    __tablename__ = "sensor_magnitudes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensores.id"),
        nullable=False,
    )
    magnitud: Mapped[str] = mapped_column(String(50), nullable=False)
    unidad: Mapped[str] = mapped_column(String(20), nullable=False)
    valor_minimo: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    valor_maximo: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))

    sensor = relationship(
        "Sensor",
        back_populates="sensor_magnitudes",
    )

    mediciones = relationship(
        "Medicion",
        back_populates="sensor_magnitud",
    )