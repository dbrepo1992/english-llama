from django.contrib import admin
from .models import Question, QuizAttempt

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'difficulty', 'created_at')
    list_filter = ('difficulty',)
    search_fields = ('question_text',)

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'difficulty', 'created_at')
    list_filter = ('difficulty',)
