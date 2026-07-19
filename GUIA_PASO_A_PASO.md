# Guía paso a paso: CI/CD con GitHub Actions, Python y FastAPI — sin Docker

## 1. Propósito de la actividad

En esta actividad se construirá una API pequeña con FastAPI y se configurará un proceso automatizado de integración y despliegue.

Al finalizar, cada estudiante tendrá:

1. Un proyecto Python funcionando en su computador.
2. Un repositorio Git local.
3. El proyecto publicado en GitHub.
4. Pruebas automáticas para dos endpoints.
5. Un workflow de GitHub Actions que revisa el código y ejecuta las pruebas.
6. Un reporte descargable generado por GitHub Actions.
7. Opcionalmente, una API publicada en Internet mediante Render, sin utilizar Docker.

## 2. ¿Qué significan CI y CD?

### Integración continua — CI

CI significa *Continuous Integration* o integración continua. Cada vez que se envía código al repositorio, GitHub Actions ejecutará automáticamente controles como:

- instalar las dependencias;
- revisar problemas básicos de calidad;
- ejecutar las pruebas;
- informar si el proyecto aprobó o falló.

### Despliegue continuo — CD

CD puede significar entrega continua o despliegue continuo. En esta guía se utilizará como despliegue continuo: si las pruebas terminan correctamente y el cambio fue enviado a la rama `main`, GitHub Actions solicitará a Render que publique la nueva versión.

La secuencia será:

```text
Computador del estudiante
        ↓ git push
Repositorio de GitHub
        ↓
GitHub Actions ejecuta CI
        ↓ solo si todo está correcto
Render despliega la API
        ↓
URL pública de la aplicación
```

> Regla central: no se debe desplegar una versión que no haya aprobado sus pruebas.

---

## 3. Requisitos previos

Cada estudiante necesita:

- una cuenta de GitHub;
- Git instalado;
- Python 3.12 o compatible;
- Visual Studio Code u otro editor;
- acceso a PowerShell;
- conexión a Internet;
- para la etapa CD, una cuenta de Render.

### 3.1 Verificar Python

Abra PowerShell y ejecute:

```powershell
py --version
```

También puede probar:

```powershell
python --version
```

El resultado debería mostrar una versión de Python instalada.

### 3.2 Verificar Git

```powershell
git --version
```

### 3.3 Configurar nombre y correo de Git

Este paso se realiza una sola vez por computador:

```powershell
git config --global user.name "Nombre Apellido"
git config --global user.email "correo-usado-en-github@ejemplo.com"
```

Para comprobar la configuración:

```powershell
git config --global --list
```

---

## 4. Crear el proyecto

### 4.1 Crear y abrir la carpeta

```powershell
mkdir fastapi-ci-cd-demo
cd fastapi-ci-cd-demo
code .
```

Si el comando `code` no está disponible, abra Visual Studio Code manualmente y seleccione la carpeta.

### 4.2 Crear un entorno virtual

```powershell
py -m venv .venv
```

Activarlo:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cuando esté activo, PowerShell mostrará normalmente `(.venv)` al inicio de la línea.

Si PowerShell bloquea la activación, ejecute lo siguiente en esa misma ventana y vuelva a intentarlo:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Esta modificación se aplica solamente a la ventana actual.

### 4.3 Crear la estructura de carpetas

Desde Visual Studio Code, cree esta estructura:

```text
fastapi-ci-cd-demo/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_api.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

Los nombres deben respetarse exactamente, especialmente `.github/workflows`.

---

## 5. Crear la API

### 5.1 Archivo `app/__init__.py`

Puede quedar vacío o contener:

```python
"""Aplicación de ejemplo para la guía de GitHub Actions."""
```

### 5.2 Archivo `app/main.py`

```python
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
```

### 5.3 ¿Qué endpoints se crearon?

| Método | Ruta | Propósito | Ejemplo esperado |
|---|---|---|---|
| GET | `/` | Información inicial | `{"mensaje":"API funcionando"...}` |
| GET | `/health` | Revisar disponibilidad | `{"status":"ok"}` |
| GET | `/doble/{numero}` | Función de negocio simple | `/doble/7` produce `14` |

El endpoint `/health` no realiza una operación compleja. Su objetivo es permitir que una persona o sistema compruebe rápidamente que la API responde.

---

## 6. Definir dependencias

### 6.1 Archivo `requirements.txt`

Incluye solamente las dependencias necesarias para ejecutar la API:

```text
fastapi>=0.115,<1.0
uvicorn[standard]>=0.30,<1.0
```

### 6.2 Archivo `requirements-dev.txt`

Incluye herramientas necesarias para desarrollar y probar:

```text
-r requirements.txt
httpx>=0.27,<1.0
pytest>=8,<10
ruff>=0.8,<1.0
```

La línea `-r requirements.txt` indica que primero se instalan las dependencias normales y después las herramientas de desarrollo.

### 6.3 Instalar dependencias

Con el entorno virtual activo:

```powershell
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

---

## 7. Ejecutar la API localmente

```powershell
uvicorn app.main:app --reload
```

Significado del comando:

- `app.main`: archivo `main.py` dentro de la carpeta `app`;
- `app`: variable que contiene la aplicación FastAPI;
- `--reload`: reinicia el servidor cuando cambia el código, útil durante el desarrollo.

Pruebe en el navegador:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
http://127.0.0.1:8000/doble/7
http://127.0.0.1:8000/docs
```

La ruta `/docs` muestra Swagger UI y permite probar la API desde el navegador.

Para detener el servidor, regrese a PowerShell y presione `Ctrl + C`.

---

## 8. Crear pruebas automatizadas

FastAPI permite probar endpoints mediante `TestClient`, sin necesidad de iniciar manualmente un servidor web.

Cree `tests/test_api.py`:

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_responde_correctamente() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_endpoint_doble_calcula_resultado() -> None:
    response = client.get("/doble/7")

    assert response.status_code == 200
    assert response.json() == {"numero": 7.0, "resultado": 14.0}


def test_endpoint_doble_rechaza_texto() -> None:
    response = client.get("/doble/hola")

    assert response.status_code == 422
```

### 8.1 Ejecutar las pruebas

```powershell
pytest -v
```

Resultado esperado:

```text
3 passed
```

### 8.2 Ejecutar revisión de calidad

```powershell
ruff check .
```

Resultado esperado:

```text
All checks passed!
```

### 8.3 Interpretación de los `assert`

Un `assert` expresa una condición que debe cumplirse:

```python
assert response.status_code == 200
```

Si la condición es verdadera, la prueba continúa. Si es falsa, la prueba falla y GitHub Actions marcará la ejecución en rojo.

---

## 9. Configurar Pytest y Ruff

Cree `pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
addopts = "-ra"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B"]
```

Este archivo ayuda a que las herramientas usen una configuración común tanto en el computador como en GitHub Actions.

---

## 10. Evitar subir archivos innecesarios

Cree `.gitignore`:

```gitignore
.venv/
venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.env
.env.*
.vscode/
.idea/
.DS_Store
Thumbs.db
reportes/
```

Nunca suba al repositorio:

- el entorno virtual `.venv`;
- contraseñas;
- tokens;
- claves privadas;
- archivos `.env` con secretos.

---

## 11. Crear el repositorio Git local

Desde la raíz del proyecto:

```powershell
git init
git branch -M main
git status
```

Agregar archivos:

```powershell
git add .
```

Crear el primer commit:

```powershell
git commit -m "feat: crear API FastAPI con pruebas"
```

Comprobar:

```powershell
git status
```

El mensaje esperado es similar a:

```text
nothing to commit, working tree clean
```

---

## 12. Crear el repositorio en GitHub

1. Ingrese a GitHub.
2. Seleccione **New repository**.
3. Use un nombre como `fastapi-ci-cd-demo`.
4. Seleccione repositorio público o privado según indique el docente.
5. No marque la creación automática de README, `.gitignore` ni licencia, porque esos archivos ya existen localmente.
6. Seleccione **Create repository**.

GitHub mostrará la dirección del repositorio. Ejemplo genérico:

```text
https://github.com/USUARIO/fastapi-ci-cd-demo.git
```

Conecte el proyecto local, reemplazando `USUARIO`:

```powershell
git remote add origin https://github.com/USUARIO/fastapi-ci-cd-demo.git
git push -u origin main
```

Git puede abrir el navegador para autenticar la cuenta.

Compruebe el remoto:

```powershell
git remote -v
```

---

## 13. Crear el primer workflow de GitHub Actions — CI

GitHub Actions busca workflows en la carpeta:

```text
.github/workflows/
```

Cree `.github/workflows/ci.yml`:

```yaml
name: CI - FastAPI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  calidad-y-pruebas:
    name: Revisar código y ejecutar pruebas
    runs-on: ubuntu-latest

    steps:
      - name: Descargar el repositorio
        uses: actions/checkout@v6

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
          cache-dependency-path: requirements-dev.txt

      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Revisar calidad del código con Ruff
        run: ruff check .

      - name: Ejecutar pruebas automatizadas
        run: |
          mkdir -p reportes
          pytest -v --junitxml=reportes/pytest.xml

      - name: Guardar reporte de pruebas
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: reporte-pruebas
          path: reportes/
          if-no-files-found: warn
          retention-days: 14
```

> YAML depende de la indentación. Use espacios y no tabulaciones.

### 13.1 ¿Qué realiza el workflow?

| Parte | Función |
|---|---|
| `on` | Indica cuándo ejecutar el workflow |
| `push` | Se ejecuta al enviar cambios a `main` |
| `pull_request` | Se ejecuta al solicitar integrar cambios a `main` |
| `workflow_dispatch` | Permite ejecutarlo manualmente |
| `runs-on` | Crea temporalmente una máquina Ubuntu |
| `checkout` | Descarga el código del repositorio |
| `setup-python` | Configura Python 3.12 |
| `ruff check` | Revisa errores y calidad básica |
| `pytest` | Ejecuta las pruebas |
| `upload-artifact` | Conserva el reporte de pruebas para descargarlo |

### 13.2 Subir el workflow

```powershell
git add .github/workflows/ci.yml
git commit -m "ci: agregar workflow de pruebas automáticas"
git push
```

### 13.3 Revisar la ejecución

1. Abra el repositorio en GitHub.
2. Seleccione la pestaña **Actions**.
3. Abra el workflow **CI - FastAPI**.
4. Abra la ejecución más reciente.
5. Revise cada paso.

Un círculo o visto verde indica que el proceso aprobó. Una X roja indica un error.

En la parte inferior de la ejecución aparecerá el artefacto `reporte-pruebas`, que puede descargarse como evidencia.

---

## 14. Realizar una prueba de fallo controlado

Es importante demostrar que el workflow no solamente aparece en verde, sino que realmente detecta errores.

En `tests/test_api.py`, cambie temporalmente:

```python
assert response.json() == {"numero": 7.0, "resultado": 14.0}
```

por:

```python
assert response.json() == {"numero": 7.0, "resultado": 15.0}
```

Suba el cambio:

```powershell
git add tests/test_api.py
git commit -m "test: provocar fallo controlado"
git push
```

GitHub Actions debería fallar y mostrar la diferencia entre `14.0` y `15.0`.

Después restaure el valor correcto y vuelva a subirlo:

```powershell
git add tests/test_api.py
git commit -m "fix: corregir prueba del endpoint doble"
git push
```

La nueva ejecución debe quedar verde.

Esta evidencia demuestra que la automatización está verificando el software.

---

# PARTE II — CD sin Docker mediante Render

## 15. ¿Por qué se utilizará Render?

Render puede ejecutar directamente aplicaciones Python desde un repositorio Git. Para este ejercicio no es necesario crear una imagen Docker.

El servicio instalará `requirements.txt` y ejecutará Uvicorn con la aplicación FastAPI.

La versión gratuita es apropiada para aprendizaje y pruebas, pero tiene limitaciones y no debe considerarse una configuración productiva.

---

## 16. Crear el servicio web en Render

1. Ingrese o cree una cuenta en Render.
2. Conecte su cuenta de GitHub.
3. Seleccione **New** y después **Web Service**.
4. Seleccione el repositorio `fastapi-ci-cd-demo`.
5. Configure el servicio.

Valores recomendados:

| Campo | Valor |
|---|---|
| Name | Un nombre único, por ejemplo `api-fastapi-nombre-apellido` |
| Language o Runtime | Python 3 |
| Branch | `main` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Plan | Free, solamente para esta actividad |

Seleccione una región disponible apropiada para el ejercicio.

Inicie la creación del servicio. Render realizará un primer despliegue y entregará una dirección similar a:

```text
https://api-fastapi-nombre-apellido.onrender.com
```

Pruebe:

```text
https://SU-SERVICIO.onrender.com/health
https://SU-SERVICIO.onrender.com/doble/7
https://SU-SERVICIO.onrender.com/docs
```

El endpoint `/health` debe responder:

```json
{"status":"ok"}
```

---

## 17. Evitar que Render despliegue antes de aprobar CI

Render puede redesplegar automáticamente cuando detecta un `push`. Para esta actividad se quiere que GitHub Actions controle ese momento.

En la configuración del servicio:

1. Busque la opción **Auto-Deploy** o equivalente.
2. Desactívela después del primer despliegue.

De esta manera, un `push` no publicará inmediatamente el código. Primero deberá aprobar GitHub Actions y después se llamará al Deploy Hook.

---

## 18. Crear el Deploy Hook

Un Deploy Hook es una dirección privada que permite solicitar un despliegue mediante una petición HTTP.

En Render:

1. Abra el servicio.
2. Ingrese a **Settings**.
3. Busque **Deploy Hook**.
4. Cree o copie la URL del hook asociado a la rama `main`.
5. No publique esa dirección ni la escriba dentro del código.

Trátela como una contraseña: quien tenga esa URL puede iniciar un despliegue.

---

## 19. Guardar el Deploy Hook como secreto de GitHub

En el repositorio de GitHub:

1. Seleccione **Settings**.
2. En el menú lateral, abra **Secrets and variables**.
3. Seleccione **Actions**.
4. Abra la sección **Secrets**.
5. Seleccione **New repository secret**.
6. En **Name**, escriba exactamente:

```text
RENDER_DEPLOY_HOOK_URL
```

7. En **Secret**, pegue la URL entregada por Render.
8. Guarde el secreto.

El secreto no debe agregarse a `main.py`, `.env`, README ni al historial de Git.

---

## 20. Transformar el workflow de CI en CI/CD

Reemplace el contenido de `.github/workflows/ci.yml` por:

```yaml
name: CI-CD - FastAPI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  calidad-y-pruebas:
    name: CI - Revisar código y ejecutar pruebas
    runs-on: ubuntu-latest

    steps:
      - name: Descargar el repositorio
        uses: actions/checkout@v6

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
          cache-dependency-path: requirements-dev.txt

      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Revisar calidad del código con Ruff
        run: ruff check .

      - name: Ejecutar pruebas automatizadas
        run: |
          mkdir -p reportes
          pytest -v --junitxml=reportes/pytest.xml

      - name: Guardar reporte de pruebas
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: reporte-pruebas
          path: reportes/
          if-no-files-found: warn
          retention-days: 14

  desplegar:
    name: CD - Solicitar despliegue en Render
    needs: calidad-y-pruebas
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest

    steps:
      - name: Activar Deploy Hook de Render
        env:
          RENDER_DEPLOY_HOOK_URL: ${{ secrets.RENDER_DEPLOY_HOOK_URL }}
        run: |
          if [ -z "$RENDER_DEPLOY_HOOK_URL" ]; then
            echo "::error::Falta configurar el secreto RENDER_DEPLOY_HOOK_URL"
            exit 1
          fi

          curl --fail --show-error --silent \
            --request POST \
            "$RENDER_DEPLOY_HOOK_URL"

          echo "Solicitud de despliegue enviada correctamente a Render."
```

### 20.1 Elementos importantes del CD

```yaml
needs: calidad-y-pruebas
```

Significa que el despliegue depende del trabajo de pruebas. Si CI falla, el trabajo `desplegar` no se ejecuta.

```yaml
if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

Impide desplegar desde una pull request. El despliegue solamente ocurre después de un `push` real a `main`.

```yaml
${{ secrets.RENDER_DEPLOY_HOOK_URL }}
```

Recupera el valor secreto sin escribirlo directamente en el workflow.

---

## 21. Probar el despliegue continuo

Cambie en `app/main.py`:

```python
version="1.0.0",
```

por:

```python
version="1.1.0",
```

También puede cambiar el mensaje inicial.

Después:

```powershell
git add .
git commit -m "feat: actualizar versión de la API"
git push
```

Revise en este orden:

1. GitHub → pestaña **Actions**.
2. Trabajo `CI - Revisar código y ejecutar pruebas`.
3. Trabajo `CD - Solicitar despliegue en Render`.
4. Render → historial o eventos del servicio.
5. URL pública → `/docs` o `/health`.

El Deploy Hook inicia el despliegue, pero Render puede necesitar un momento para construir e iniciar la nueva versión. La ejecución verde de GitHub confirma que la solicitud fue aceptada; el estado final del servicio se verifica en Render y en la URL pública.

---

## 22. Comprobar que una versión incorrecta no se despliega

1. Vuelva a provocar un fallo en una prueba.
2. Haga commit y push.
3. Confirme que el trabajo de CI aparece en rojo.
4. Confirme que el trabajo de despliegue aparece omitido.
5. Corrija la prueba y vuelva a subirla.

Esta es la evidencia principal de una canalización CI/CD correctamente protegida.

---

## 23. Solución de problemas frecuentes

### `python` o `py` no se reconoce

Python no está instalado o no fue agregado al PATH. Reinstálelo marcando la opción correspondiente o use el comando que sí funcione entre `py` y `python`.

### PowerShell impide activar `.venv`

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### `ModuleNotFoundError: No module named 'fastapi'`

Active el entorno virtual e instale las dependencias:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

### `pytest` no encuentra `app`

Compruebe que:

- está ejecutando el comando desde la raíz del proyecto;
- existe `app/__init__.py`;
- `pyproject.toml` contiene `pythonpath = ["."]`.

### GitHub Actions no aparece

Compruebe que el archivo esté exactamente en:

```text
.github/workflows/ci.yml
```

También revise que el archivo haya sido incluido en un commit y enviado con `git push`.

### El workflow muestra un error YAML

Revise la indentación. YAML usa espacios; no use tabulaciones.

### Falla `ruff check .`

Ejecute localmente:

```powershell
ruff check .
```

Para corregir automáticamente ciertos problemas:

```powershell
ruff check . --fix
```

Revise los cambios antes de crear el commit.

### Falla el trabajo de despliegue por secreto ausente

Cree en GitHub el secreto con el nombre exacto:

```text
RENDER_DEPLOY_HOOK_URL
```

### Render indica que no encuentra la aplicación

Revise el Start Command:

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

No cambie `$PORT` por un número fijo, porque la plataforma entrega ese valor mediante una variable de entorno.

### La API gratuita tarda en responder

Un servicio gratuito puede suspenderse por inactividad y tardar más en la primera respuesta. Esto no necesariamente significa que la aplicación esté dañada.

---

## 24. Evidencias que debe entregar el estudiante

La entrega sugerida contiene:

1. URL del repositorio GitHub.
2. README con instrucciones de ejecución.
3. Captura de `pytest -v` ejecutado localmente.
4. Captura de una ejecución verde en GitHub Actions.
5. Captura de una ejecución roja provocada intencionalmente.
6. Captura posterior de la corrección y nueva ejecución verde.
7. Artefacto o reporte de pruebas descargado desde Actions.
8. URL pública de Render.
9. Captura de `/health` funcionando en la URL pública.
10. Captura de Swagger UI en `/docs`.
11. Breve explicación de qué impide que se despliegue código con pruebas fallidas.

---

## 25. Criterios de evaluación sugeridos — 100 puntos

| Criterio | Puntaje |
|---|---:|
| Proyecto Python organizado y ejecutable | 10 |
| Endpoint `/health` correcto | 8 |
| Endpoint funcional `/doble/{numero}` | 8 |
| Pruebas automatizadas suficientes | 14 |
| Uso correcto de Git y commits comprensibles | 10 |
| Repositorio GitHub completo y ordenado | 10 |
| Workflow CI instala, revisa y prueba | 15 |
| Evidencia de fallo controlado y corrección | 10 |
| CD ejecutado solamente después de aprobar CI | 10 |
| README y evidencias finales | 5 |
| **Total** | **100** |

Si todavía no se evaluará despliegue externo, los 10 puntos de CD pueden reasignarse a pruebas, documentación y calidad del repositorio.

---

## 26. Desafíos de ampliación

Después de completar la actividad básica, se puede solicitar:

- agregar un endpoint `POST /sumar`;
- validar datos mediante un modelo de Pydantic;
- agregar pruebas para entradas inválidas;
- usar ramas y pull requests;
- impedir cambios directos en `main` mediante reglas de protección;
- mostrar el badge del workflow en el README;
- ejecutar pruebas con más de una versión de Python;
- agregar cobertura de pruebas;
- incorporar Docker en una unidad posterior.

---

## 27. Conclusión

En esta actividad el estudiante no solamente publica código. Construye una canalización verificable:

```text
Código → Git → GitHub → revisión automática → pruebas → despliegue
```

El aprendizaje central es que la automatización debe actuar como una barrera de calidad. Una modificación no debería llegar al entorno publicado si no cumple las condiciones definidas por el equipo.
