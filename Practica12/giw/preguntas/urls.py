from django.urls import path

from . import views

app_name = "preguntas"

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginFunction, name='login'),
    path('logout', views.logoutFunction, name='logout'),
    path('nueva_pregunta', views.nueva_pregunta, name='nueva_pregunta'),
    path('<int:question_id>/', views.pregunta_n, name='pregunta_n'),

    #path('')
]