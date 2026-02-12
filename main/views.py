from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Answer, QuizSession, UserAnswer, models
from django.contrib.auth.decorators import login_required

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'main/quiz_list.html', {'quizzes': quizzes})



@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    session = QuizSession.objects.create(quiz=quiz, user=request.user)
    return redirect('quiz_question', session_id=session.id, question_index=0)


@login_required
def quiz_question(request, session_id, question_index):
    session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    questions = list(session.quiz.question_set.all())

    if question_index >= len(questions):
        session.completed = True
        session.finished_at = models.DateTimeField(auto_now=True)
        session.save()
        return redirect('quiz_result', session_id=session.id)

    question = questions[question_index]
    if request.method == 'POST':
        answer_id = int(request.POST.get('answer'))
        answer = Answer.objects.get(id=answer_id)
        is_correct = answer.is_correct
        UserAnswer.objects.create(
            session=session,
            question=question,
            selected_answer=answer,
            is_correct=is_correct
        )
        if is_correct:
            session.score += 1
            session.save()
        return redirect('quiz_question', session_id=session.id, question_index=question_index+1)

    return render(request, 'main/quiz_question.html', {'question': question, 'session': session})


@login_required
def quiz_result(request, session_id):
    session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    user_answers = UserAnswer.objects.filter(session=session)
    return render(request, 'main/quiz_result.html', {'session': session, 'user_answers': user_answers})
