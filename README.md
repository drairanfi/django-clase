# django-clase

Repositorio de la clase de Django de la universidad. Acá vas a trabajar las
actividades de la materia y a seguir el [tutorial oficial de Django][tutorial]
(en este momento, el estado del repo corresponde a la parte 1: `mysite`
creado con `django-admin startproject` y la app `polls` recién inicializada).

## Stack

- Python 3.14
- Django 6.1
- SQLite (base por defecto, no requiere configuración)

## Estructura

```
mysite/        Proyecto Django (settings, urls raíz, wsgi/asgi)
polls/         App del tutorial (encuestas)
explicaciones/ Resúmenes de cada clase (clase-NN.md + plantilla.md)
manage.py      Script de gestión de Django
```

Cada clase deja un resumen en `explicaciones/clase-NN.md`. No hay que
«inventar» historia: cada resumen respeta la plantilla y registra solo lo que
se hizo en esa clase.

## Puesta en marcha

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install django
python manage.py migrate
python manage.py runserver
```

Abrí http://127.0.0.1:8000/ para ver el proyecto y http://127.0.0.1:8000/admin/
para el panel de administración.

## Comandos útiles

```bash
python manage.py runserver            # servidor de desarrollo
python manage.py migrate              # aplica migraciones
python manage.py makemigrations polls # genera migraciones nuevas
python manage.py test                 # corre los tests
```

## Resúmenes de clase

Cada clase se documenta en `explicaciones/clase-NN.md` (ver `plantilla.md`).
- Clase 1: setup del repo + parte 1 del tutorial

## Progreso del tutorial

- [x] Parte 1: proyect + app (crear `mysite` y `polls`)
- [ ] Parte 2: modelos, admin, migraciones
- [ ] Parte 3: views y templates
- [ ] Parte 4: forms y generic views
- [ ] Parte 5: testing
- [ ] Parte 6: static files
- [ ] Parte 7: personalizar el admin

## Actividades de la clase

(Pendiente: cada actividad se documenta acá a medida que se entrega.)

[tutorial]: https://docs.djangoproject.com/en/6.1/intro/tutorial01/