# Clase 3 — Parte 2 desde el shell: Choices, `choice_set` y el admin

- **Fecha:** 2026-08-29
- **Autor(es):** ambos
- **Parte del tutorial / actividad:** Tutorial parte 2 (repaso desde el shell) + admin

## Qué se hizo en la clase

- Retomamos la **parte 2**: en vez de avanzar, nos detuvimos a entender cómo se
  trabaja con los modelos desde el shell.
- Aprendimos a crear `Choice` desde la consola y a recorrer la relación entre
  `Question` y `Choice` con la API de Django.
- Registramos `Choice` en el admin (quedaba pendiente de la clase 2).

---

## Parte 2 (repaso) — Trabajar con los modelos desde el shell

### Idea de la parte

Los modelos ya son tablas en la base, pero hasta ahora solo los tocamos desde
el admin. El shell es la **consola interactiva de Django**: nos deja probar
consultas y crear/borrar datos escribiendo Python, sin navegador. Es la
"prueba de fuego" de que los modelos están bien definidos.

### Paso a paso (qué hicimos)

1. **Entrar al shell:**

   ```bash
   python manage.py shell
   ```

2. **Verificar que `__str__` funciona y probar las consultas básicas.** `filter`
   devuelve un `QuerySet` (lista), siempre con `filter` por palabra clave:

   ```python
   >>> from polls.models import Question, Choice
   >>> Question.objects.all()
   <QuerySet [<Question: What's up?>]>

   >>> Question.objects.filter(id=1)
   <QuerySet [<Question: What's up?>]>
   >>> Question.objects.filter(question_text__startswith="What")
   <QuerySet [<Question: What's up?>]>
   ```

3. **Buscar la pregunta publicada este año.** `get` devuelve un solo objeto:

   ```python
   >>> from django.utils import timezone
   >>> current_year = timezone.now().year
   >>> Question.objects.get(pub_date__year=current_year)
   <Question: What's up?>
   ```

4. **Pedir un id que no existe.** `get` no se queda en silencio: lanza la
   excepción `DoesNotExist`:

   ```python
   >>> Question.objects.get(id=2)
   Traceback (most recent call last):
       ...
   DoesNotExist: Question matching query does not exist.
   ```

5. **Atajo por clave primaria.** `pk` es igual que `id`, pero más corto y
   genérico:

   ```python
   >>> Question.objects.get(pk=1)
   <Question: What's up?>
   ```

6. **Probar el método custom del modelo:**

   ```python
   >>> q = Question.objects.get(pk=1)
   >>> q.was_published_recently()
   True
   ```

7. **Crear `Choice` desde el `Question`.** Django crea solo `choice_set`, la
   relación inversa de la `ForeignKey`: "los choices de esta pregunta".
   `create()` arma el objeto, hace el `INSERT` y te devuelve el `Choice` nuevo:

   ```python
   >>> q.choice_set.all()
   <QuerySet []>

   >>> q.choice_set.create(choice_text="Not much", votes=0)
   <Choice: Not much>
   >>> q.choice_set.create(choice_text="The sky", votes=0)
   <Choice: The sky>
   >>> c = q.choice_set.create(choice_text="Just hacking again", votes=0)
   ```

8. **Recorrer la relación para los dos lados:**

   ```python
   >>> c.question
   <Question: What's up?>

   >>> q.choice_set.all()
   <QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
   >>> q.choice_set.count()
   3
   ```

9. **Consultas que atraviesan relaciones** con doble guión bajo (`__`). No hay
   límite de profundidad: todos los `Choice` de las preguntas publicadas este
   año:

   ```python
   >>> Choice.objects.filter(question__pub_date__year=current_year)
   <QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
   ```

10. **Borrar un objeto con `delete()`:**

    ```python
    >>> c = q.choice_set.filter(choice_text__startswith="Just hacking")
    >>> c.delete()
    ```

11. **Registrar `Choice` en el admin.** En `polls/admin.py`:

    ```python
    from django.contrib import admin

    from .models import Question, Choice

    admin.site.register(Question)
    admin.site.register(Choice)
    ```

    Ahora en http://127.0.0.1:8000/admin/ también se pueden crear y editar
    opciones.

### Conceptos clave (en simple)

- **`QuerySet`**: "lista perezosa" de objetos de la base. No consulta hasta que
  lo necesitás (cuando lo imprimís, lo iterás, etc.).
- **`filter` vs `get`**: `filter` devuelve un `QuerySet` (puede tener 0, 1 o
  muchos), `get` devuelve un solo objeto y si no existe revienta con
  `DoesNotExist`.
- **`pk`**: abreviatura de "primary key". En nuestros modelos es `id`, pero
  con `pk` no dependés de cómo se llame la clave.
- **`choice_set`**: Django crea solo el "otro lado" de una `ForeignKey`. Te da
  los `Choice` de una `Question` (`.all()`, `.count()`, `.filter()`...).
- **`create()`**: atajo que hace `constructor + save()` en un paso.
- **Doble guión bajo (`__`)**: sirve para atravesar relaciones en las consultas
  (`question__pub_date__year`) o usar búsquedas especiales
  (`question_text__startswith`).
- **`DoesNotExist`**: no es un bug. Es la forma que tiene `get` de avisarte que
  "no existe nada con eso". Si querés que no reviente, usá `filter`.
- **`delete()`**: borra el objeto. Si borrás una `Question`, sus `Choice` se
  borran en cascada (por el `on_delete=models.CASCADE`).

### Error típico / lección

Que `get()` lance `DoesNotExist` parece un error, pero es **comportamiento
esperado**: está protegiendo al código para que no use un objeto que no existe.
La lección de fondo: elegir `filter` o `get` según lo que necesites, no según
lo que "funcione sin quejarse".

(Sigue vigente la lección de la clase 2: si editas `models.py`, el shell **no
recarga solo** — `exit()` y volvé a entrar.)

### Qué quedó funcionando

- Base con datos cargados: 2 preguntas y sus opciones (ej: "¿qué desayunaste?"
  con "Huevos rancheros" y "Salchipapa").
- `Choice` visible y editable en http://127.0.0.1:8000/admin/.
- Quedó **resuelto el pendiente de la clase 2** (cargar datos de `Choice` para
  ver `choice_set.all` y el admin).

---

## Comandos usados en la clase

```bash
python manage.py shell
python manage.py runserver
```

## Dudas / pendientes

- `tests.py` sigue vacío; los tests llegan en la parte 5.
- Probar más consultas con `__` (ej: buscar por texto de la `Choice`).

## Siguiente paso

- Parte 4: formulario de votación en `detail.html`, vista `vote` que procesa el
  POST, y views genéricas (`ListView`/`DetailView`).