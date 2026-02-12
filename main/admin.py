from django.contrib import admin
from .models import Quiz, Question, Answer, QuizSession, UserAnswer
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
admin.site.register(Quiz)
admin.site.register(Question, inlines=[AnswerInline])
admin.site.register(QuizSession)
admin.site.register(UserAnswer)
