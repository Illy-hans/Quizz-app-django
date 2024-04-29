from django.utils.safestring import mark_safe
from rest_framework import serializers
from .models import QuestionsDB, Quizzes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect details")