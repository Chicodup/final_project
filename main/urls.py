from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('quiz/<int:quiz_id>/questions/add/', views.add_questions, name='add_questions'),
    path('quiz/<int:quiz_id>/questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    path('quiz/<int:quiz_id>/admin-results/', views.quiz_results_admin, name='quiz_results_admin'),
    path('quiz/<int:quiz_id>/enter-name/', views.enter_name, name='enter_name'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('session/<int:session_id>/question/<int:question_index>/', views.quiz_question, name='quiz_question'),
    path('session/<int:session_id>/result/', views.quiz_result, name='quiz_result'),
]