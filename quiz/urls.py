from django.urls import path
from .views import QuizView
from django.views.generic import TemplateView

app_name = "quiz"

urlpatterns = [
    path("", TemplateView.as_view(template_name="quiz/quiz_start.html"), name="quiz-start"),
    path("play/", QuizView.as_view(), name="quiz_game"),
]
