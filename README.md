# API FastAPI para practicar CI/CD con GitHub Actions

Proyecto educativo mínimo que contiene:

- Endpoint `GET /health`.
- Endpoint funcional `GET /doble/{numero}`.
- Pruebas automatizadas con `pytest` y `TestClient`.
- Revisión estática con Ruff.
- Workflow de integración continua con GitHub Actions.
- Plantilla de despliegue continuo en Render sin Docker.

## Ejecución local rápida

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Documentación interactiva: `http://127.0.0.1:8000/docs`

## Pruebas

```powershell
ruff check .
pytest -v
```

## Workflows

- `.github/workflows/ci.yml`: CI inicial lista para usar.
- `docs/ci-cd-render.yml`: plantilla final de CI/CD para copiar sobre el workflow cuando Render y el secreto estén configurados.
