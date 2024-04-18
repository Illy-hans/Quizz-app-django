from django.utils.safestring import mark_safe
from rest_framework import serializers
from .models import QuestionsDB, Quizzes
from django.contrib.auth.models import User

class QuestionsDBSerializer(serializers.ModelSerializer):  
    class Meta:
        model = QuestionsDB
        fields = ["id", "category", "question", "correct_answer", "incorrect_answers"]
        # fields = '__all__'

class QuizzesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizzes
        fields = ["id", "user", "timestamp", "score", "questions"]


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ["id", "password", "username","first_name", "last_name", "email", "date_joined"]
