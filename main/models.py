from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    class Meta:
        verbose_name = "Вікторина"
        verbose_name_plural = "Вікторини"
        ordering = ['-created_at']

    title = models.CharField(max_length=255, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Дедлайн")

    def __str__(self):
        return self.title


class Question(models.Model):
    class Meta:
        verbose_name = "Питання"
        verbose_name_plural = "Питання"
        ordering = ['id']

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="Вікторина")
    text = models.TextField(verbose_name="Текст питання")
    time_limit = models.IntegerField(default=30, verbose_name="Час на відповідь (секунди)")
    media = models.FileField(upload_to='questions_media/', null=True, blank=True, verbose_name="Медіафайл")

    def __str__(self):
        return self.text


class Answer(models.Model):
    class Meta:
        verbose_name = "Відповідь"
        verbose_name_plural = "Відповіді"
        ordering = ['id']

    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Питання")
    text = models.CharField(max_length=255, verbose_name="Текст відповіді")
    is_correct = models.BooleanField(default=False, verbose_name="Правильна відповідь")

    def __str__(self):
        return self.text


class QuizSession(models.Model):
    class Meta:
        verbose_name = "Сесія вікторини"
        verbose_name_plural = "Сесії вікторин"
        ordering = ['-started_at']

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="Вікторина")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач", null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    score = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    player_name = models.CharField(max_length=100, default='Гравець')

    def __str__(self):
        return f"{self.quiz.title} - {self.player_name}"


class UserAnswer(models.Model):
    class Meta:
        verbose_name = "Відповідь користувача"
        verbose_name_plural = "Відповіді користувачів"

    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)