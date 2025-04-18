from django.views import View
from django.shortcuts import render
from openai import OpenAI
import os
import re

class QuizStartView(View):
    template_name = "quiz/quiz_start.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        topic = request.POST.get("topic")
        prompt = f"Create a short English quiz on the topic: {topic}. Include 5 multiple-choice questions with 4 answer options (A-D)."

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        raw_text = response.choices[0].message.content.strip()
        questions = self.parse_quiz_text(raw_text)

        return render(request, "quiz/quiz_game.html", {
            "topic": topic,
            "questions": questions
        })

    def parse_quiz_text(self, text):
        blocks = re.split(r'\n(?=\d+\.)', text)  # Split by question numbers like "1."
        parsed_questions = []

        for block in blocks:
            lines = block.strip().split("\n")
            if not lines:
                continue
            question = lines[0].strip()
            options = [line.strip() for line in lines[1:] if line.strip()]
            parsed_questions.append({
                "question": question,
                "options": options
            })

        return parsed_questions
