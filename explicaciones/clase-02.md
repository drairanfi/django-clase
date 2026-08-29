# Clase 2 — Tutorial partes 2 y 3: modelos, admin, vistas y templates

- **Fecha:** 2026-08-22
- **Autor(es):** ambos
- **Parte del tutorial / actividad:** Tutorial partes 2 y 3

## Qué se hizo en la clase

- Parte 2: definimos los modelos `Question` y `Choice`, los convertimos en
  tablas (migraciones) y los registramos en el admin.
- Parte 3: escribimos vistas que consultan la base y templates que muestran
  las preguntas en HTML.

---

## Parte 2 — Modelos, migraciones y el admin

### Idea de la parte

Hasta acá el sitio solo devolvía texto fijo. El objetivo: **guardar preguntas
y opciones en una base de datos** y poder verlas/crearlas desde un panel web.

### Paso a paso (qué hicimos)

1. **Vincular la app al proyecto.** En `mysite/settings.py`, dentro de la
   lista `INSTALLED_APPS`, agregá al principio:

   ```python
   "polls.apps.PollsConfig",
   ```

2. **Definir los modelos.** En `polls/models.py` (reemplazando todo):

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

3. **Crear la migración y aplicarla** (genera y ejecuta el "plano" de la base):

   ```bash
   python manage.py makemigrations polls
   python manage.py migrate
   ```

4. **Probar los modelos con el shell** (consola interactiva de Django):

   ```bash
   python manage.py shell
   ```
  4.1 **Importante** : Ejecutar import de los modelos que se quiere buscar ya que se puede perder la referencia

   ```python
   >>> from polls.models import Question, Choice
   >>> from django.utils import timezone
   >>> q = Question(question_text="What's new?", pub_date=timezone.now())
   >>> q.save()
   >>> Question.objects.all()
   <QuerySet [<Question: What's new?>]>
   ```

5. **Registrar el modelo en el admin.** En `polls/admin.py`:

   ```python
   from django.contrib import admin

   from .models import Question

   admin.site.register(Question)
   ```

   Creá un super usuario y entrá al panel:

   ```bash
   python manage.py createsuperuser
   ```

   Abrí http://127.0.0.1:8000/admin/ → vas a poder crear y ver preguntas.

### Conceptos clave (en simple)

- **Modelo = tabla**: cada clase que hereda de `models.Model` es una tabla de
  la base. Cada atributo (`CharField`, `DateTimeField`, `IntegerField`) es una
  columna.
- **Migración**: la "receta" que dice cómo crear/cambiar la base.
  `makemigrations` genera la receta, `migrate` la ejecuta.
- **`__str__`**: define cómo se muestra un objeto cuando lo imprimís (en el
  shell, admin, etc.). Sin él verías "Question object (1)".
- **`ForeignKey`**: la relación "una `Question` tiene muchas `Choice`". Se
  declara en `Choice` apuntando a `Question`.
- **Admin**: Django genera un panel de gestión gratis por cada modelo
  registrado.
- **Shell**: consola con Python + Django cargados, para probar sin navegador.

### Error típico / lección

El shell **no recarga solo los cambios** del código. Si editás `models.py`
con la consola abierta, sigue usando la clase vieja (en memoria) y tira
errores raros (ej: "no attribute" o "unexpected keyword arguments"). Solución:
`exit()` y volver a entrar. La primera vez nos pasó y nos hizo dudar del
código cuando el código estaba bien.

### Qué quedó funcionando

- Tablas `polls_question` y `polls_choice` creadas (migración `0001_initial`).
- `Question` visible y editable en http://127.0.0.1:8000/admin/.

---

## Parte 3 — Vistas y templates

### Idea de la parte

Ahora que hay datos, hay que **mostrarlos en páginas HTML** en vez de texto
plano. Se separa la lógica (views) del diseño (templates).

### Paso a paso (qué hicimos)

1. **Escribir las vistas.** En `polls/views.py` (reemplazando todo):

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

2. **Configurar las URLs.** En `polls/urls.py` (reemplazando todo):

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

3. **Crear el template del listado.** En `polls/templates/polls/index.html`
   (crear la carpeta si no existe):

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

5. **Probar en el navegador:**

   - http://127.0.0.1:8000/polls/ → lista las preguntas con links.
   - http://127.0.0.1:8000/polls/1/ → muestra la pregunta 1 y sus opciones.

### Conceptos clave (en simple)

- **Vista**: función que recibe el `request` y devuelve la respuesta. "La
  lógica de la página".
- **Template**: archivo HTML con lógica mínima (`{% if %}`, `{% for %}`,
  `{{ variable }}`). "El diseño de la página".
- **`render()`**: junta request + template + datos (contexto) y devuelve la
  página armada.
- **`get_object_or_404()`**: busca un objeto; si no existe devuelve un 404
  limpio (en vez de reventar).
- **`<int:question_id>`**: la URL "atrapa" un entero y lo pasa a la vista
  como argumento.
- **`{% url 'polls:detail' question.id %}`**: genera el link sin escribirlo a
  mano. `app_name = "polls"` permite el prefijo `polls:`.
- **`choice_set`**: Django crea solo la relación inversa de una `ForeignKey`;
  trae todas las `Choice` de una `Question`.

### Error típico / lección

Al reescribir `views.py` nos quedó sin el import de `HttpResponse` y las
vistas `results`/`vote` reventaban con `NameError`. Lección: al editar un
archivo, revisar siempre que los imports correspondan a lo que se usa.

### Qué quedó funcionando

- `/polls/` lista las últimas 5 preguntas.
- `/polls/<id>/` muestra la pregunta con sus opciones.

---

## Comandos usados en la clase

```bash
python manage.py makemigrations polls
python manage.py migrate
python manage.py shell
python manage.py createsuperuser
python manage.py runserver
```

## Dudas / pendientes

- Cargar datos de ejemplo de `Choice` para ver `choice_set.all` y el admin.
- `tests.py` sigue vacío; los tests llegan en la parte 5.

## Siguiente paso

- Parte 4: formulario de votación en `detail.html`, vista `vote` que procesa
  el POST, y views genéricas (`ListView`/`DetailView`).