import django
from django.db import models
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

from .models import Pregunta, Respuesta
from .forms import LoginForm, QuestionForm, AnswerForm

@require_GET
def index(request):
    """Muestra todas las preguntas"""
    preguntas = Pregunta.objects.order_by('-question_date')
    return render(request, "preguntas.html", {'preguntas': preguntas})

@require_http_methods(["GET", "POST"])
def loginFunction(request):
    """Loguea al usuario"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {'login_form': form})

    form = LoginForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('preguntas:index'))
    else:
        return HttpResponseBadRequest("Usuario o contraseña incorrectos")

@require_GET
def logoutFunction(request):
    """Elimina al usuario de la sesión actual"""
    logout(request)
    return redirect(reverse('preguntas:index'))


@login_required(login_url='preguntas:login')
@require_http_methods(["GET", "POST"])
def nueva_pregunta(request):
    """Muestra el formulario de nueva pregunta (GET) o recibe el formulario y añade la pregunta (POST)"""
    if request.method == "GET":
        form = QuestionForm()
        return render(request, "nueva_pregunta.html", {'question_form': form})

    form = QuestionForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")
    texto_f = form.cleaned_data['texto']
    tit_f = form.cleaned_data['titulo']

    # Crea un objeto ORM a partir de los datos limpios del formulario y lo salva en la BD
    question = Pregunta(question_title=tit_f, question_text=texto_f, question_author=request.user)
    question.save()

    return redirect(reverse('preguntas:index'))

@login_required(login_url='preguntas:login')
@require_http_methods(["GET"])
def pregunta_n(request, question_id):
    """Muestra la pregunta número n"""
    pregunta = get_object_or_404(Pregunta, pk = question_id)

    respuestas =  Respuesta.objects.filter(question=pregunta)
    
    return render(request, "pregunta.html", {'pregunta': pregunta, 'respuestas:':respuestas})

    ##return redirect(reverse('preguntas:index'))
    #form = AnswerForm(request.POST)
    #if not form.is_valid():
        #return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")
    #texto_f = form.cleaned_data['respuesta']
    
    #answer = Respuesta(answer_text = texto_f, answer_author=request.user, question=pregunta)
    #answer.save()
    