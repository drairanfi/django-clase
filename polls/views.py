from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

def detail(request, question_id):
    return HttpResponse("Estas mirando la pregunta con id: %s." % question_id)


def results(request, question_id):
    response = "Estas mirando los resultados de la pregunta con id: %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("Estas votando en la pregunta con id: %s." % question_id)

def preguntas(request):
    question = Question.objects.get(id=2)
    return HttpResponse(question.question_text)
