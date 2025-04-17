import openai
from django.views.generic import TemplateView
from django.shortcuts import render
from .models import Question

openai.api_key = "your_openai_key_here"  # Use env variable in production

class QuizStartView(TemplateView):
    template_name = "quiz/quiz_start.html"

    def post(self, request, *args, **kwargs):
        topic = request.POST.get("topic")
        difficulty = request.POST.get("difficulty")

        prompt = f"""
        Create a multiple-choice English question about {topic}, difficulty: {difficulty}.
        Format:
        Question: ...
        A) ...
        B) ...
        C) ...
        D) ...
        Correct: A/B/C/D
        """

        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.7,
            max_tokens=200
        )

        generated = response.choices[0].text.strip()
        lines = generated.split("\n")

        question_text = lines[0].replace("Question: ", "")
        options = {line[0]: line[3:].strip() for line in lines[1:5]}
        correct_option = lines[5].split(":")[1].strip()

        # Save to DB
        Question.objects.create(
            question_text=question_text,
            option_a=options["A"],
            option_b=options["B"],
            option_c=options["C"],
            option_d=options["D"],
            correct_option=correct_option,
            difficulty=difficulty
        )

        return render(request, "quiz/quiz_start.html", {
            "success": "Question generated and saved!"
        })
