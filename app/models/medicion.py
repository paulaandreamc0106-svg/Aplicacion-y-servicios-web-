from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Medicion(Base):
    __tablename__ = "mediciones"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sensor_magnitud_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sensor_magnitudes.id"),
        nullable=False,
    )
    valor: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )
    timestamp_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    fecha_recepcion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    sensor_magnitud = relationship(
        "SensorMagnitud",
        back_populates="mediciones",
    )