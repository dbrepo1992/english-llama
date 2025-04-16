# quiz/views.py
from django.shortcuts import render, redirect
from django.views import View
from .models import Question
import random

class QuizView(View):
    def get(self, request):
        difficulty = request.GET.get("difficulty", "easy")
        questions = list(Question.objects.filter(difficulty=difficulty))

        if not questions:
            return render(request, "quiz/quiz_game.html", {
                "question": None,
                "difficulty": difficulty
            })

        question = random.choice(questions)
        return render(request, "quiz/quiz_game.html", {
            "question": question,
            "difficulty": difficulty
        })

    def post(self, request):
        selected_answer = request.POST.get("answer")
        question_id = request.POST.get("question_id")
        difficulty = request.POST.get("difficulty")
        question = Question.objects.get(id=question_id)

        correct = selected_answer == question.correct_answer
        result_message = "✅ Correct!" if correct else f"❌ Correct answer: {question.correct_answer}"

        return render(request, "quiz/quiz_game.html", {
            "question": question,
            "difficulty": difficulty,
            "result_message": result_message,
            "show_result": True
        })
