from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *
from django.contrib import admin

urlpatterns = [
    # versioning down the road: v1/......

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Database Questions
    path("questionsdb/", QuestionsDBListCreate.as_view(), name="add/view-questions"),
    path("questionsdb/<int:pk>/", QuestionsDBRetrieveUpdateDestroy.as_view(), name="retrieve-update-destroy-questions"),
    path("questionsdb/add", AddQuestionsAPIView.as_view(), name="add-questions-to-database"),

# quizzes are also protected by a token!
    #Quiz DB
    path("quizzes/", QuizzesListCreate.as_view(), name="add/view-quizzes"),
    path("quizzes/<int:pk>/", QuizzesRetrieveUpdateDestroy.as_view(), name="retrieve-update-destroy-quizzes"),

# user is protected by a token
    # User DB
    path("users/", UserListCreate.as_view(), name="add/view-users"),
    path("users/<int:pk>", UserRetrieveUpdateDestroy.as_view(), name="retrieve-update-destroy-users"),
    path("users/login", UserLoginAPIView.as_view(), name="login-user"),
    path("users/logout", UserLogoutAPIView.as_view(), name="logout-user")
]