from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.sensores import router as sensores_router
from app.api.sensor_magnitudes import router as sensor_magnitudes_router
from app.api.mediciones import router as mediciones_router
from app.mqtt.client import iniciar_mqtt, detener_mqtt


@asynccontextmanager
async def lifespan(app: FastAPI):
    iniciar_mqtt()
    yield
    detener_mqtt()


app = FastAPI(
    title="API IoT - Taller 2",
    description="API para adquisición, validación y consulta de datos IoT",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(sensores_router)
app.include_router(sensor_magnitudes_router)
app.include_router(mediciones_router)


@app.get("/")
def inicio():
    return {"mensaje": "API IoT funcionando correctamente"}