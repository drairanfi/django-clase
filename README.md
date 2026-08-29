# django-clase

Proyecto de la **clase de Django** de la universidad. Lo armamos siguiendo el
[tutorial oficial de Django][tutorial](`Writing your first Django app`) junto
con las actividades de la materia.

La idea de este README es que puedas **arrancar desde cero** y avanzar **parte
por parte**, copiando y pegando. Cada parte del tutorial está explicada como
si no supieras nada de Django (que es justo el caso 😉).

No hace falta leerlo todo seguido: agarrá donde venís y seguí.

---

## Stack (qué usa el proyecto)

- **Python 3.14** — el lenguaje.
- **Django 6.1** — el framework web.
- **SQLite** — la base de datos (viene de fábrica, no configuramos nada).

---

## Conceptos antes de empezar (30 segundos)

- **Proyecto** (`mysite`): el sitio web completo, una caja que agrupa
  configuraciones, la base, las URLs raíz. Se crea una sola vez.
- **App** (`polls`): una "parte funcional" del sitio (acá, las encuestas).
  Un proyecto puede tener varias apps.
- **Modelo**: la descripción de una tabla en la base, como clases Python
  (`Question`, `Choice`).
- **Vista**: la función que recibe un *request* (pedido) y devuelve un
  *response* (respuesta).
- **Template**: archivo HTML con lógica mínima, donde se dibuja la página.
- **URL**: la regla que conecta *https://.../encuesta/1/* con una vista.

---

## Puesta en marcha (una sola vez)

Para arrancar el proyecto en una máquina nueva (esto es lo primero que hacés):

**macOS / Linux:**

```bash
python3 -m venv .venv                          # 1. crear el entorno virtual
source .venv/bin/activate                      # 2. activarlo
pip install django                             # 3. instalar Django
python manage.py migrate                       # 4. crear la base con las apps internas de Django
python manage.py runserver                     # 5. levantar el servidor de desarrollo
```

**Windows — CMD:**

```bat
py -m venv .venv                               # 1. crear el entorno virtual
.venv\Scripts\activate.bat                     # 2. activarlo
pip install django                             # 3. instalar Django
python manage.py migrate                       # 4. crear la base con las apps internas de Django
python manage.py runserver                     # 5. levantar el servidor de desarrollo
```

**Windows — PowerShell:**

```powershell
py -m venv .venv                               # 1. crear el entorno virtual
.venv\Scripts\Activate.ps1                     # 2. activarlo
pip install django                             # 3. instalar Django
python manage.py migrate                       # 4. crear la base con las apps internas de Django
python manage.py runserver                     # 5. levantar el servidor de desarrollo
```

> Si en Windows no tenés el comando `py` o `python`, instalá Python desde
> python.org y marcá la opción "Add Python to PATH" durante la instalación.
>
> Si PowerShell no te deja activar el venv, ejecutá una vez:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.

Abrí http://127.0.0.1:8000/ para ver el sitio y
http://127.0.0.1:8000/admin/ para el panel de administración (créale un super
usuario con `python manage.py createsuperuser`).

> Desde ahora, **siempre activá el venv primero** antes de cualquier comando:
> `source .venv/bin/activate` (macOS/Linux) o `.venv\Scripts\activate.bat`
> (Windows), y usá el servidor con `python manage.py runserver`.

---

## El tutorial, parte por parte

### ✅ Parte 1 — Crear el proyecto y la primera app

**Objetivo:** tener un sitio Django que responda.

**Qué se hizo:**

1. Crear el proyecto:

   ```bash
   django-admin startproject mysite
   ```

   Esto crea la carpeta `mysite/` con `settings.py` (configuración), `urls.py`
   (rutas raíz), `wsgi.py` y `asgi.py` (cómo se sirve el sitio).

2. Crear la app:

   ```bash
   python manage.py startapp polls
   ```

   Crea la carpeta `polls/` con los archivos base (por ahora casi vacíos:
   `models.py`, `views.py`, `admin.py`, ...).

3. Escribir la primera vista. En `polls/views.py`:

   ```python
   from django.http import HttpResponse

   def index(request):
       return HttpResponse("Hello, world. You're at the polls index.")
   ```

4. Conectarla por URL. Creá `polls/urls.py`:

   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path("", views.index, name="index"),
   ]
   ```

5. Decirle al proyecto que use las URLs de la app. En `mysite/urls.py`:

   ```python
   from django.contrib import admin
   from django.urls import include, path

   urlpatterns = [
       path("polls/", include("polls.urls")),
       path("admin/", admin.site.urls),
   ]
   ```

6. Probar: con el servidor corriendo, abrí http://127.0.0.1:8000/polls/
   → deberías ver el mensaje *"Hello, world..."*.

**Concepto de la parte:** proyecto vs app, y el *flow* completo
URL → vista → respuesta.

---

### ✅ Parte 2 — Modelos, migraciones y el admin

**Objetivo:** definir las tablas (`Question` / `Choice`), crearlas en la base
y verlas en el panel de admin.

1. **Vincular la app** al proyecto. En `mysite/settings.py`, dentro de la
   lista `INSTALLED_APPS`, agregá al principio:

   ```python
   "polls.apps.PollsConfig",
   ```

2. **Definir los modelos.** En `polls/models.py`:

   ```python
   import datetime

   from django.db import models
   from django.utils import timezone


   class Question(models.Model):
       question_text = models.CharField(max_length=200)
       pub_date = models.DateTimeField("date published")

       def __str__(self):
           return self.question_text

       def was_published_recently(self):
           return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


   class Choice(models.Model):
       question = models.ForeignKey(Question, on_delete=models.CASCADE)
       choice_text = models.CharField(max_length=200)
       votes = models.IntegerField(default=0)

       def __str__(self):
           return self.choice_text
   ```

3. **Crear la migración** (la "receta" de cómo construir la tabla):

   ```bash
   python manage.py makemigrations polls
   python manage.py migrate
   ```

4. **Probar en la consola interactiva** de Django (el "shell"):

   ```bash
   python manage.py shell
   ```

   ```python
   >>> from polls.models import Question, Choice
   >>> from django.utils import timezone
   >>> q = Question(question_text="What's new?", pub_date=timezone.now())
   >>> q.save()
   >>> Question.objects.all()
   <QuerySet [<Question: What's new?>]>
   ```

   > ⚠️ El shell **no recarga solo** los cambios. Si tocaste `models.py` con
   > la consola abierta, salí (`exit()`) y volvé a entrar.
   >
   > ⚠️ **Guarda**: `q.save()` es lo que escribe en la base. Si no lo llamás,
   > el objeto solo vive en memoria.

5. **Registrar el modelo en el admin.** En `polls/admin.py`:

   ```python
   from django.contrib import admin
   from .models import Question

   admin.site.register(Question)
   ```

   Creá un super usuario y entrá a http://127.0.0.1:8000/admin/:

   ```bash
   python manage.py createsuperuser
   ```

**Concepto de la parte:** los modelos son clases Python que Django convierte
en tablas (migraciones), y el admin es gratis (lo genera solo).

---

### ✅ Parte 3 — Vistas y templates

**Objetivo:** que `/polls/` liste las preguntas y `/polls/<id>/` muestre el
detalle, usando plantillas HTML.

1. **Escribir las vistas.** En `polls/views.py`:

   ```python
   from django.http import HttpResponse
   from django.shortcuts import get_object_or_404, render

   from .models import Question


   def index(request):
       latest_question_list = Question.objects.order_by("-pub_date")[:5]
       context = {"latest_question_list": latest_question_list}
       return render(request, "polls/index.html", context)


   def detail(request, question_id):
       question = get_object_or_404(Question, pk=question_id)
       return render(request, "polls/detail.html", {"question": question})


   def results(request, question_id):
       response = "You're looking at the results of question %s."
       return HttpResponse(response % question_id)


   def vote(request, question_id):
       return HttpResponse("You're voting on question %s." % question_id)
   ```

2. **Agregar las URLs.** En `polls/urls.py`:

   ```python
   from django.urls import path

   from . import views

   app_name = "polls"
   urlpatterns = [
       path("", views.index, name="index"),
       path("<int:question_id>/", views.detail, name="detail"),
       path("<int:question_id>/results/", views.results, name="results"),
       path("<int:question_id>/vote/", views.vote, name="vote"),
   ]
   ```

3. **Crear la carpeta de templates** y el listado. En
   `polls/templates/polls/index.html`:

   ```html
   {% if latest_question_list %}
       <ul>
       {% for question in latest_question_list %}
           <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
       {% endfor %}
       </ul>
   {% else %}
       <p>No polls are available.</p>
   {% endif %}
   ```

4. **Crear el template de detalle.** En `polls/templates/polls/detail.html`:

   ```html
   {{ question }}

   <h1>{{ question.question_text }}</h1>
   <ul>
   {% for choice in question.choice_set.all %}
       <li>{{ choice.choice_text }}</li>
   {% endfor %}
   </ul>
   ```

5. Probar: http://127.0.0.1:8000/polls/ y http://127.0.0.1:8000/polls/1/

**Conceptos de la parte:**
- **`render()`**: junta un request + template + datos, y devuelve la página.
- **`get_object_or_404()`**: busca un objeto y si no existe devuelve un error
  **404** (en vez de chocar).
- **`<int:question_id>`**: die que la URL lleva un número entero.
- **`{% url 'polls:detail' id %}`**: arma las URLs en el template sin
  hardcodearlas (`app_name` nos da `polls:<nombre>`).

---

### ⏭️ Parte 4 — Formularios y views genéricas (próximo paso)

Después de la parte 3 el tutorial agrega el formulario de votación en el
template de detalle, una vista que registre el voto, y después remplaza las
vistas por **views genéricas** (menos código repetido).

Seguimos por acá en la próxima clase.

---

## Progreso del tutorial

- [x] **Parte 1**: crear proyecto y app, primera vista
- [x] **Parte 2**: modelos `Question`/`Choice`, migraciones, admin
- [x] **Parte 3**: vistas y templates
- [ ] **Parte 4**: formularios y views genéricas
- [ ] **Parte 5**: tests
- [ ] **Parte 6**: archivos estáticos (CSS)
- [ ] **Parte 7**: personalizar el admin

## Actividades de la clase

(Pendiente: cada actividad se documenta acá a medida que se entrega.)

## Resúmenes de clase

Cada clase se registra en `explicaciones/clase-NN.md` (ver `plantilla.md`):

- [Clase 01](explicaciones/clase-01.md) — setup del repo + parte 1
- [Clase 02](explicaciones/clase-02.md) — tutorial partes 2 y 3
- [Clase 03](explicaciones/clase-03.md) — parte 2 desde el shell: Choices y `choice_set`

## Estructura del repo

```
mysite/        El proyecto Django (settings, urls raíz, wsgi/asgi)
polls/         La app de encuestas (modelos, vistas, urls, templates)
explicaciones/ Los resúmenes por clase
manage.py      Script para los comandos de Django
```

## Comandos útiles

```bash
python manage.py runserver             # servidor de desarrollo
python manage.py makemigrations polls  # nueva migración de la app polls
python manage.py migrate               # aplicar migraciones
python manage.py createsuperuser       # crear usuario del admin
python manage.py test                  # correr los tests
```

[tutorial]: https://docs.djangoproject.com/en/6.1/intro/tutorial01/