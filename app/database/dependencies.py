from collections.abc import Generator

from app.database.connection import SessionLocal


def obtener_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()