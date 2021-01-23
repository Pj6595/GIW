from django.db import models
from django.conf import settings

class Pregunta(models.Model):
    question_title = models.CharField(max_length=250)
    question_text = models.CharField(max_length=5000)
    question_date = models.DateTimeField(auto_now_add=True)
    question_author = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, on_delete=models.SET_NULL)
    #answer_number = models.IntegerField(default=0)
    def __str__(self):
        return self.question_title

class Respuesta(models.Model):
    question = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=5000)
    answer_date = models.DateTimeField(auto_now_add=True)
    answer_author = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.answer_text
    