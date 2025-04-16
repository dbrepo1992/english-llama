from django.contrib import admin
from .models import Question, QuizAttempt

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "difficulty", "created_at")
    list_filter = ("difficulty",)
    search_fields = ("text",)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "score", "difficulty", "created_at", "is_correct")
    list_filter = ("difficulty", "created_at", "is_correct")
