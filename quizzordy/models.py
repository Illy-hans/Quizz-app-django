from django.db import models
from django.contrib.auth.models import User
from django.db import models

class QuestionsDB(models.Model):
    category = models.CharField(max_length=200)
    question = models.CharField(max_length=400)
    correct_answer = models.CharField(max_length=400)
    incorrect_answers = models.JSONField()

class Quizzes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(max_length=4)
    questions = models.ManyToManyField(QuestionsDB)

