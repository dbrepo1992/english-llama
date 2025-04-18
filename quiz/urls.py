# quiz/urls.py
from django.urls import path
from .views import QuizStartView

app_name = "quiz"

urlpatterns = [
    path("", QuizStartView.as_view(), name="quiz-start"),
]
