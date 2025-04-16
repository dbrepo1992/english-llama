from django.shortcuts import render
from django.views import View

class QuizView(View):
    def get(self, request):
        question = {
            "text": "What is the capital of France?",
            "options": {
                "A": "Berlin",
                "B": "Madrid",
                "C": "Paris",
                "D": "Rome",
            },
            "correct": "C"
        }
        return render(request, "quiz/quiz_game.html", {"question": question})
