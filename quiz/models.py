from django.db import models
from django.contrib.auth.models import User

DIFFICULTY_LEVELS = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
]

class Question(models.Model):
    text = models.CharField(max_length=255)
    options = models.JSONField()
    correct = models.CharField(max_length=1)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='easy')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_options(self):
        options = [self.correct_answer] + self.incorrect_answers
        random.shuffle(options)
        return options

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected = models.CharField(max_length=1)
    is_correct = models.BooleanField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.text} - {self.score}"
