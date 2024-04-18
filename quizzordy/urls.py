from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from django.contrib import admin

urlpatterns = [
    # versioning down the road: v1/......

    # admin 
    path('admin/', admin.site.urls),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Database Questions
    path("questionsdb/", views.QuestionsDBListCreate.as_view(), name="add/view-questions"),
    path("questionsdb/<int:pk>/", views.QuestionsDBRetrieveUpdateDestroy.as_view(), name="retrieve-update-destroy-questions"),
    path("questionsdb/add", views.add),

# quizzes are also protected by a token!
    #Quiz DB
    path("quizzes/", views.QuizzesListCreate.as_view(), name="add/view-quizzes"),
    path("quizzes/<int:pk>/", views.QuizzesRetrieveUpdateDestroy.as_view(), name="retrieve-update-destroy-quizzes"),

# user is protected by a token
    # User DB
    path("users/", views.UserListCreate.as_view(), name="add/view-users"),
    path("users/<int:pk>", views.UserRetrieveUpdateDestroy.as_view(), name="retrieve-update-destroy-users")

]