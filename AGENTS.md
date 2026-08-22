# AGENTS.md

Guía para agentes de IA (y colaboradores) que trabajen en este repo.

## Qué es este repo

Un proyecto de clase que sigue el **tutorial oficial de Django** (proyecto
`mysite`, app `polls`). El objetivo es pedagógico: aprender Django siguiendo
el tutorial y resolviendo actividades de la materia. NO es una app de
producción ni una base de código preexistente compleja.

## Reglas de oro

1. **Seguí el tutorial oficial paso a paso.** Cada cambio debe ser el paso
   natural siguiente del tutorial o cumplir con una consigna de clase.
   No saltees etapas ni agregues patrones avanzados que el tutorial aún no
   cubrió.
2. **No "mejores" lo que ya funciona solo porque sí.** Si el código es
   didáctico y correcto para su etapa, dejalo así. La prioridad es el
   aprendizaje, no la arquitectura de producción.
3. **Mantené la simplicidad.** Usá solo lo que el tutorial provee: `path()`,
   `HttpResponse`, templates con la herarquía por defecto, `django.test`.
   Sin DRF, sin autenticación custom, sin librerías de terceros salvo que la
   clase lo pida.
4. **Cada decisión de código se explica en las clases.** Si un cambio se sale
   del tutorial, que sea porque hay una actividad de la materia detrás.

## Resúmenes de clase (`explicaciones/`)

Cada clase genera un resumen en `explicaciones/clase-NN.md` usando la
plantilla `explicaciones/plantilla.md`. Reglas:

- Nombre del archivo: `clase-01.md`, `clase-02.md`, etc. Sin acentos ni
  caracteres especiales.
- Se escribe en español, al final de la clase o antes de la siguiente.
- Registra fecha, autor(es), qué se hizo, conceptos clave, comandos,
  pendientes y el siguiente paso. No pegar código entero.
- Este es un trabajo EN EQUIPO: los resúmenes deben reflejar lo que hicieron
  ambos compañeros, no solo una persona.

## Manejo de ramas

- Somos dos personas trabajando el repo en ramas separadas.
- Cada uno trabaja su rama; `main` es la rama compartida con lo aprobado.
- Antes de crear una rama, traer los últimos cambios: `git pull origin main`.
- Un cambio se integra a `main` cuando está terminado y, preferentemente,
  revisado por el otro compañero (pull request).
- Evitar mergear a `main` desde la consola con `git merge` directo si se puede
  abrir un PR.
- `explicaciones/` se trabaja también por PR; no pisar resúmenes del otro.

## Comandos

```bash
python manage.py runserver            # servidor de desarrollo
python manage.py makemigrations polls # nuevas migraciones
python manage.py migrate              # aplicar migraciones
python manage.py test                 # correr tests
```

## Convenciones

- Python 3.14, Django 6.1. Código con estilo estándar de Django/PEP 8.
- Los tests se escriben según el patrón del tutorial (clases `TestCase` en
  `polls/tests.py`).
- Nombres de migraciones y modelos en inglés, siguiendo el tutorial
  (`Question`, `Choice`).
- No subir secretos. La `SECRET_KEY` de desarrollo ya viene generada; no la
  reemplazar por una real en debug.

## Estado actual (checkpoint)

- Parte 1 completa: `mysite` + `polls` creados, URL `/polls/` responde.
- `polls` aún NO está en `INSTALLED_APPS`.
- `polls/models.py` está vacío (próximo paso: modelos `Question`/`Choice`).

## Estructura

```
mysite/        Proyecto Django (settings, urls raíz, wsgi/asgi)
polls/         App del tutorial (encuestas)
explicaciones/ Resúmenes de cada clase (clase-NN.md + plantilla.md)
```

## Referencias

- Tutorial: https://docs.djangoproject.com/en/6.1/intro/tutorial01/