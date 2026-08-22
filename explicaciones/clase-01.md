# Clase 1 — Setup del repo y parte 1 del tutorial

- **Fecha:** 2026-08-22
- **Autor(es):** ambos (primer día)
- **Parte del tutorial / actividad:** Tutorial parte 1 + documentación del repo

## Qué se hizo en la clase

- Se creó el proyecto `mysite` con `django-admin startproject`.
- Se creó la app `polls` con `startapp` y una primera vista `index`.
- Se conectó la app al proyecto por URL (`/polls/`).
- Se documentó y acondicionó el repo: `README.md`, `AGENTS.md`, `.gitignore`.

---

## Parte 1 — Crear el proyecto y la primera app

### Idea de la parte

Que el sitio de Django exista y responda algo cuando entramos a una URL. Acá
se arma la caja (proyecto), se agrega una cajita adentro (app) y se hace que
responda.

### Paso a paso (qué hicimos)

1. **Crear el entorno virtual** (aisla las librerías del sistema) y activarlo:

   **macOS / Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows — CMD:**

   ```bat
   py -m venv .venv
   .venv\Scripts\activate.bat
   ```

   **Windows — PowerShell:**

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   > En Windows, si PowerShell bloquea la activación, corré una vez:
   > `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.

2. **Instalar Django** dentro del entorno:

   ```bash
   pip install django
   ```

3. **Crear el proyecto** (la caja completa del sitio):

   ```bash
   django-admin startproject mysite
   ```

4. **Crear la app** (la parte funcional "encuestas"):

   ```bash
   python manage.py startapp polls
   ```

5. **Escribir la primera vista.** En `polls/views.py` (reemplazando todo):

   ```python
   from django.http import HttpResponse

   def index(request):
       return HttpResponse("Hello, world. You're at the polls index.")
   ```

6. **Crear las URLs de la app.** Creá `polls/urls.py`:

   ```python
   from django.urls import path

   from . import views

   urlpatterns = [
       path("", views.index, name="index"),
   ]
   ```

7. **Conectar las URLs de la app al proyecto.** En `mysite/urls.py`:

   ```python
   from django.contrib import admin
   from django.urls import include, path

   urlpatterns = [
       path("polls/", include("polls.urls")),
       path("admin/", admin.site.urls),
   ]
   ```

8. **Levantar el servidor** y probar:

   ```bash
   python manage.py runserver
   ```

   Abrí http://127.0.0.1:8000/polls/ → deberías ver
   *"Hello, world. You're at the polls index."*

### Conceptos clave (en simple)

- **Proyecto vs app**: el proyecto es el sitio completo (`mysite`, se crea una
  sola vez); la app es una parte funcional del sitio (`polls`). Un proyecto
  puede tener muchas apps.
- **Vista**: la función que recibe el pedido del navegador (`request`) y
  devuelve una respuesta (`response`). Acá, un texto.
- **URL → vista**: el archivo `urls.py` conecta una dirección web con una
  vista. El proyecto delega en la app con `include()`.
- **VENV**: carpeta invisible que guarda las librerías del proyecto para no
  ensuciar el sistema. Hay que activarla antes de usar `python`.

### Error típico / lección

Ninguno en la parte 1. Sí una regla de oro: **siempre activar el venv** antes
de cualquier `python manage.py ...`, si no, usás un Python que no tiene Django.

### Qué quedó funcionando

- http://127.0.0.1:8000/polls/ responde el texto de `index`.

---

## Comandos usados en la clase

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows — CMD:**

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

**Windows — PowerShell:**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**Comunes (después de activar el venv):**

```bash
pip install django
django-admin startproject mysite
python manage.py startapp polls
python manage.py runserver
```

## Dudas / pendientes

- Adopción de las ramas entre los dos (ver AGENTS.md): crear rama propia antes
  de tocar código compartido.

## Siguiente paso

- Parte 2: modelos `Question` y `Choice`, agregar `polls` a `INSTALLED_APPS`,
  primeras migraciones y el panel de admin.