from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('start/<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    path('session/<int:session_id>/question/<int:question_index>/', views.quiz_question, name='quiz_question'),
    path('session/<int:session_id>/result/', views.quiz_result, name='quiz_result'),
]
