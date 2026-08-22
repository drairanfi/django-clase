# Clase 1 — Setup del repo y parte 1 del tutorial

- **Fecha:** 2026-08-22
- **Autor(es):** ambos (primer día)
- **Parte del tutorial / actividad:** Tutorial parte 1 + documentación del repo

## Qué se hizo

- Se creó el proyecto `mysite` con `django-admin startproject` y la app `polls`
  con `startapp`.
- Se configuró la URL `/polls/` que responde con la vista `index`.
- Se documentó el repo: `README.md` (guía para humanos) y `AGENTS.md` (guía
  para agentes de IA que trabajen el repo).
- Se agregó `.gitignore` y se dejó de trackear `db.sqlite3` y `__pycache__/`.
- Se creó la carpeta `explicaciones/` con su plantilla para registrar cada
  clase.

## Conceptos clave

- **Proyecto vs app:** el proyecto es el sitio completo (`mysite`), la app es
  una parte funcional (encuestas = `polls`).
- **urls.py:** cómo Django enruta una petición a una vista (primero la raíz,
  después la app con `include()`).
- **views.py:** dónde vive la lógica de una vista; por ahora devuelve un
  `HttpResponse` básico.
- **VENV:** entorno virtual para aislar dependencias del sistema.

## Comandos usados

```bash
python -m venv .venv
pip install django
django-admin startproject mysite
python manage.py startapp polls
python manage.py runserver
```

## Código resultante

- `mysite/urls.py` incluye `polls.urls` bajo la ruta `polls/`.
- `polls/urls.py` enruta `/polls/` hacia `views.index`.
- `polls/views.py` tiene una vista `index` mínima (`HttpResponse`).
- `polls/models.py` aún está vacío: los modelos se ven en la parte 2.

## Dudas / pendientes

- ¿Por qué `polls` todavía no está en `INSTALLED_APPS`? → Se agrega cuando
  aparezcan los modelos (parte 2).
- Confirmar cómo trabajamos las ramas entre los dos (ver AGENTS.md).

## Siguiente paso

- Parte 2 del tutorial: modelos `Question` y `Choice`, agregar `polls` a
  `INSTALLED_APPS`, primeras migraciones y el panel de admin.