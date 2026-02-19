from django.contrib import admin
from .models import Quiz, Question, Answer, QuizSession, UserAnswer

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ('question', 'selected_answer', 'is_correct', 'answered_at', 'correct_answer')

    def correct_answer(self, obj):
        return obj.question.answers.filter(is_correct=True).first()
    correct_answer.short_description = "Правильна відповідь"

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at')
    inlines = [QuestionInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'time_limit')
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'score', 'completed', 'started_at', 'finished_at')
    readonly_fields = ('started_at', 'finished_at')
    inlines = [UserAnswerInline]

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'question', 'selected_answer', 'is_correct', 'answered_at', 'correct_answer')
    readonly_fields = ('answered_at', 'correct_answer')

    def correct_answer(self, obj):
        return obj.question.answers.filter(is_correct=True).first()
    correct_answer.short_description = "Правильна відповідь"
