# Clase 4 — Parte 4: formulario de votación y views genéricas

- **Fecha:** 2026-09-26
- **Autor(es):** ambos
- **Parte del tutorial / actividad:** Tutorial parte 4

## Qué se hizo en la clase

- Agregamos el **formulario de votación** en `polls/detail.html` (radio buttons
  que mandan `choice=<id>` por POST).
- Escribimos la vista **`vote()` de verdad** (hasta ahora era un mensaje
  fijo), con `F("votes") + 1`, manejo del caso "no eligió nada" y redirección.
- Creamos el template **`polls/results.html`** que muestra los resultados.
- Reemplazamos las vistas `index`, `detail` y `results` por **views
  genéricas** (`ListView` / `DetailView`), como pide el tutorial.
- Verificamos todo con el **cliente de tests** de Django (votar suma 1 voto y
  redirige a los resultados).

---

## Parte 4 (a) — El formulario de votación

### Idea de la parte

Hasta ahora el sitio solo **mostraba** datos. Esta parte agrega lo que falta
para que sea una app de verdad: que el usuario pueda **votar** y **ver el
resultado**. Eso implica un formulario en HTML, una vista que procese el POST
y un template que muestre el conteo.

### Paso a paso (qué hicimos)

1. **El formulario en el template de detalle.** En
   `polls/templates/polls/detail.html`:

   ```html
   <form action="{% url 'polls:vote' question.id %}" method="post">
   {% csrf_token %}
   <fieldset>
       <legend><h1>{{ question.question_text }}</h1></legend>
       {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
       {% for choice in question.choice_set.all %}
           <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
           <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
       {% endfor %}
   </fieldset>
   <input type="submit" value="Vote">
   </form>
   ```

   - Cada radio manda `choice=<id>` al servidor. El `name="choice"` es la
     clave que después leemos con `request.POST["choice"]`.
   - `method="post"`: votar **modifica datos**, así que va por POST (GET es
     solo para leer).
   - `{% csrf_token %}`: protege el POST contra Cross Site Request Forgery.
   - `{% url 'polls:vote' question.id %}` arma la URL del formulario sin
     hardcodearla.

2. **La vista `vote` de verdad.** En `polls/views.py`:

   ```python
   from django.db.models import F
   from django.http import HttpResponse, HttpResponseRedirect
   from django.shortcuts import get_object_or_404, render
   from django.urls import reverse

   from .models import Choice, Question


   def vote(request, question_id):
       question = get_object_or_404(Question, pk=question_id)
       try:
           selected_choice = question.choice_set.get(pk=request.POST["choice"])
       except (KeyError, Choice.DoesNotExist):
           # Redisplay the question voting form.
           return render(
               request,
               "polls/detail.html",
               {
                   "question": question,
                   "error_message": "You didn't select a choice.",
               },
           )
       else:
           selected_choice.votes = F("votes") + 1
           selected_choice.save()
           # Always return an HttpResponseRedirect after successfully dealing
           # with POST data.
           return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
   ```

   - `request.POST["choice"]` es el id de la opción elegida (siempre texto).
   - Si no eligió nada → `KeyError`; si el id no existe → `Choice.DoesNotExist`.
     En ambos casos **vuelve a mostrar el formulario** con `error_message`.
   - `F("votes") + 1` suma 1 **dentro de la base de datos** (Django arma un
     `UPDATE ... SET votes = votes + 1`). No hay que traer el valor a Python.
   - `reverse("polls:results", args=(question.id,))` arma la URL destino (ej:
     `/polls/5/results/`) y `HttpResponseRedirect` manda al navegador para allá.

3. **El template de resultados.** Creá `polls/templates/polls/results.html`:

   ```html
   <h1>{{ question.question_text }}</h1>

   <ul>
   {% for choice in question.choice_set.all %}
       <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
   {% endfor %}
   </ul>

   <a href="{% url 'polls:detail' question.id %}">Vote again?</a>
   ```

   `|pluralize` agrega la "s" de *votes* automáticamente cuando hay más de uno.

### Conceptos clave (en simple)

- **POST vs GET**: GET pide datos (no cambia nada), POST envía datos que
  **modifican** el servidor (acá, un voto). Los formularios que cambian el
  estado siempre usan POST.
- **`csrf_token`**: una firma que Django exige en todo POST interno para
  evitar que otro sitio mande votos en tu nombre.
- **`F()`**: expresiones que la base resuelve sola. Evita que dos usuarios
  votando a la vez se pisen el conteo (condición de carrera).
- **`reverse()`**: arma la URL a partir del **nombre** de la vista y sus
  parámetros, en vez de escribir la URL a mano (así no se rompe si la URL
  cambia).
- **`HttpResponseRedirect` después de un POST exitoso**: si devolviéramos el
  HTML directo, apretar el botón "atrás" del navegador **re-enviaría el voto**.
  Redirigir (patrón PRG) evita el doble voto.
- **`error_message`**: es solo una variable del contexto; el template la
  muestra con `{% if error_message %}`. Acá no usamos mensajes flash del
  framework, seguimos lo del tutorial.

### Error típico / lección

Al verificar con el cliente de tests, el POST sin opción elegida respondía 200
pero el texto "didn't select a choice" **no aparecía** buscando con el apóstrofo
literal. No era un bug: Django **escapa el apóstrofo** en HTML
(`didn&#x27;t`). Lección: al buscar texto renderizado, pensar en el escape.

Otra lección práctica del entorno: con `DEBUG=True` y `ALLOWED_HOSTS=[]`, el
cliente de tests rechaza el host `testserver`. Para probar hay que pasarle
`HTTP_HOST='127.0.0.1'` (o agregar `testserver` a `ALLOWED_HOSTS`).

### Qué quedó funcionando

- http://127.0.0.1:8000/polls/5/ → formulario con las opciones de "qué
  desayunaste?".
- Votar una opción → redirige a `/polls/5/results/` y muestra los votos
  (probamos: la opción pasó de 0 a 1 voto).
- Enviar sin elegir → el formulario se re-muestra con el mensaje de error.

---

## Parte 4 (b) — Views genéricas

### Idea de la parte

`index`, `detail` y `results` hacen casi lo mismo: buscar datos según un
parámetro de la URL, cargar un template y renderizar. Django trae **views
genéricas** que ya hacen ese patrón por nosotros: `ListView` (una lista de
objetos) y `DetailView` (un solo objeto). Menos código repetido.

### Paso a paso (qué hicimos)

1. **Las views genéricas en `polls/views.py`.** Reemplazan a `index`, `detail`
   y `results`:

   ```python
   from django.db.models import F
   from django.http import HttpResponse, HttpResponseRedirect
   from django.shortcuts import get_object_or_404, render
   from django.urls import reverse
   from django.views import generic

   from .models import Choice, Question


   class IndexView(generic.ListView):
       template_name = "polls/index.html"
       context_object_name = "latest_question_list"

       def get_queryset(self):
           """Return the last five published questions."""
           return Question.objects.order_by("-pub_date")[:5]


   class DetailView(generic.DetailView):
       model = Question
       template_name = "polls/detail.html"


   class ResultsView(generic.DetailView):
       model = Question
       template_name = "polls/results.html"


   def vote(request, question_id):
       question = get_object_or_404(Question, pk=question_id)
       try:
           selected_choice = question.choice_set.get(pk=request.POST["choice"])
       except (KeyError, Choice.DoesNotExist):
           return render(
               request,
               "polls/detail.html",
               {
                   "question": question,
                   "error_message": "You didn't select a choice.",
               },
           )
       else:
           selected_choice.votes = F("votes") + 1
           selected_choice.save()
           return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
   ```

   - `IndexView` sigue devolviendo las últimas 5 preguntas pero como una
     clase que configura `get_queryset()`.
   - `DetailView`/`ResultsView` solo declaran `model = Question` y el template.
     El `get_object_or_404` lo hace Django por adentro.
   - `vote()` no se convierte: procesar un POST es lógica propia, no un caso
     "mostrar una página".

2. **Actualizar `polls/urls.py`.** Los patrones de detalle y resultados cambian
   de `<int:question_id>` a `<int:pk>`, porque `DetailView` espera que el
   parámetro de la URL se llame `pk`:

   ```python
   from django.urls import path

   from . import views

   app_name = "polls"
   urlpatterns = [
       path("", views.IndexView.as_view(), name="index"),
       path("<int:pk>/", views.DetailView.as_view(), name="detail"),
       path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
       path("<int:question_id>/vote/", views.vote, name="vote"),
       path("preguntas/", views.preguntas, name="preguntas"),
   ]
   ```

   La URL de `vote` **no cambia** de nombre de parámetro: la vista sigue siendo
   una función que recibe `question_id`.

### Conceptos clave (en simple)

- **`ListView`**: genérica para "mostrar una lista". Configura la consulta con
  `get_queryset()` y el nombre del contexto con `context_object_name`.
- **`DetailView`**: genérica para "mostrar un objeto". Usa `model = Question`,
  busca por `pk` de la URL y hace el 404 solo.
- **`template_name`**: las genéricas tienen un nombre de template por defecto
  (`polls/question_detail.html`); con `template_name` les decimos cuál usar.
- **`context_object_name`**: `ListView` manda el contexto como
  `question_list` por defecto; lo renombramos a `latest_question_list` para no
  tocar el template de la parte 3.
- **`<int:pk>`**: `DetailView` recibe el objeto buscando por clave primaria, y
  la clave debe llamarse `pk` en el patrón de URL.

### Error típico / lección

Si dejamos `<int:question_id>` en las URLs de `detail`/`results`, las views
genéricas fallan: `DetailView` espera un parámetro llamado `pk` y no encuentra
el objeto. El error se ve al navegar (el detalle deja de resolver). Por eso el
tutorial renombra el patrón a `<int:pk>` justo cuando se convierten.

### Qué quedó funcionando

- Todo lo de la parte 4 (a) sigue funcionando, pero con menos código propio.
- La vista `preguntas` (actividad de la clase 3) **se mantiene** tal cual: es
  una función con `HttpResponse`, no forma parte de las genéricas, y por eso
  conservamos `from django.http import HttpResponse`.

---

## Comandos usados en la clase

```bash
python manage.py runserver           # probar en el navegador
python manage.py check               # valida que el proyecto esté sano
python manage.py shell -c "..."      # probar el flujo con el cliente de tests
```

## Dudas / pendientes

- `tests.py` sigue vacío; los tests llegan en la **parte 5** (probar el
  comportamiento con `TestCase`, no a mano).
- En la base real quedó registrado 1 voto de prueba en "Huevos rancheros"
  (se puede resetear desde el admin o el shell).

## Siguiente paso

- **Parte 5 (tests)**: escribir `polls/tests.py` con `TestCase` (¿hay 5
  preguntas? ¿votar suma 1? ¿la vista detalle responde 404 si no existe?).