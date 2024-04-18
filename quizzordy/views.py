from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import Random
import requests
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

from .models import QuestionsDB
from .serializer import QuestionsDBSerializer

from .models import Quizzes
from .serializer import QuizzesSerializer

from django.contrib.auth.models import User
from .serializer import UserSerializer

# QUESTIONS
# This just needs to list 
class QuestionsDBListCreate(generics.ListCreateAPIView):
    queryset = QuestionsDB.objects.all()
    serializer_class = QuestionsDBSerializer

    def get(self, request, *arg, **kwargs):
        random_questions = QuestionsDB.objects.annotate(random_order=Random()).order_by('random_order')[:5]
        serializer = self.serializer_class(random_questions, many=True)
        return JsonResponse({"questions": serializer.data, "status": "200"})


    # delete function for developement
    def delete(self, request, *arg, **kwargs):
        QuestionsDB.objects.all().delete()
        return Response(status=status.HTTP_204_No_CONTENT)

class QuestionsDBRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionsDB.objects.all()
    serializer_class = QuestionsDBSerializer
    lookup_field = "pk"

def add(request):
        url = "https://opentdb.com/api.php?amount=10&category=10&difficulty=easy&type=multiple"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for result in data['results']: 
                category = result['category']
                question_text = result['question']
                correct_answer = result['correct_answer']
                incorrect_answers = result['incorrect_answers']
                
                # Create a question object using the retrieved data
                QuestionsDB.objects.create(
                    category=category,
                    question=question_text,
                    correct_answer=correct_answer,
                    incorrect_answers=incorrect_answers
                    )
            return JsonResponse({"status": 201, "message": "Questions added successfully"})
        
        else:
            return JsonResponse({"status": response.status_code, "error": "Failed to fetch data from the external API"})


# Quizzes
class QuizzesListCreate(generics.ListCreateAPIView):
    queryset = Quizzes.objects.all()
    serializer_class = QuizzesSerializer

    # FOR DEVELOPMENT - deletes all 
    def delete(self, request, *arg, **kwargs):
        Quizzes.objects.all().delete()
        return Response(status=status.HTTP_204_No_CONTENT)
    
class QuizzesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quizzes.objects.all()
    serializer_class = QuizzesSerializer
    lookup_field = "pk"

# User
class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # overrides the default create method to include password hashing 
    def create(self, request, *args, **kwargs):
        try:
            # data is copied so the password can be amended and then saved
            request_data_copy = request.data.copy()
            email = request_data_copy.get('email')
            if User.objects.filter(email=email).exists():
                return JsonResponse({"status": 400, "message": "Email is already in use"})
            
            else: 
                password = request_data_copy.get('password')
                if password:
                    # Hash the password
                    hashed_password = make_password(password)
                    # Set the hashed password in the request data
                    request_data_copy['password'] = hashed_password

                    # Call the create method
                    serializer = self.get_serializer(data=request_data_copy)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)

                    return JsonResponse({"status": 201, "message": "User added successfully"})

        except Exception as e:
            return JsonResponse({"status": 500, "message": f"Error: {e}"})
    

    # FOR DEVELOPMENT - deletes all 
    def delete(self, request, *arg, **kwargs):
        User.objects.all().delete()
        return Response(status=status.HTTP_204_No_CONTENT)


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"


