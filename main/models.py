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
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    score = models.IntegerField(default=0, verbose_name="Очки")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Час початку")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="Час завершення")
    completed = models.BooleanField(default=False, verbose_name="Завершено")

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"

class UserAnswer(models.Model):
    class Meta:
        verbose_name = "Відповідь користувача"
        verbose_name_plural = "Відповіді користувачів"
        ordering = ['answered_at']
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, verbose_name="Сесія вікторини")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Питання")
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name="Вибрана відповідь")
    is_correct = models.BooleanField(default=False, verbose_name="Правильна відповідь")
    answered_at = models.DateTimeField(auto_now_add=True, verbose_name="Час відповіді")
