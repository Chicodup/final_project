from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/questions/add/', views.add_questions, name='add_questions'),
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('session/<int:session_id>/question/<int:question_index>/', views.quiz_question, name='quiz_question'),
    path('session/<int:session_id>/result/', views.quiz_result, name='quiz_result'),
]
