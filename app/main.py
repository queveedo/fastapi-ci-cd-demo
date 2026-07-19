from fastapi import FastAPI

app = FastAPI(
    title="API de ejemplo para CI/CD",
    description="Proyecto educativo para probar GitHub Actions sin Docker.",
    version="1.0.0",
)


@app.get("/")
def inicio() -> dict[str, str]:
    """Entrega información básica de la API."""
    return {
        "mensaje": "API funcionando",
        "documentacion": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Endpoint utilizado para verificar que el servicio está disponible."""
    return {"status": "ok"}


@app.get("/doble/{numero}")
def calcular_doble(numero: float) -> dict[str, float]:
    """Calcula el doble de un número recibido en la URL."""
    return {
        "numero": numero,
        "resultado": numero * 2,
    }
