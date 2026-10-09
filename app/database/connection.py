import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("No se encontró DATABASE_URL en el archivo .env")


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL)

from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def probar_conexion():
    with engine.connect() as connection:
        resultado = connection.execute(text("SELECT 1"))
        print("Conexión exitosa a PostgreSQL.")
        print("Resultado:", resultado.scalar())


if __name__ == "__main__":
    probar_conexion()