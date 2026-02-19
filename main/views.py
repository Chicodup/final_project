from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms import modelformset_factory, inlineformset_factory
from .models import Quiz, Question, Answer, QuizSession, UserAnswer
from .forms import QuizForm, QuestionForm, AnswerForm

# Inline formset для додавання відповідей до питання
AnswerFormSet = inlineformset_factory(
    Question, Answer, form=AnswerForm, extra=4, can_delete=True
)

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'main/quiz_list.html', {
        'quizzes': quizzes,
        'welcome_text': "Ласкаво просимо! Оберіть вікторину або створіть свою."
    })

@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.creator = request.user
            quiz.save()
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'main/create_quiz.html', {'form': form})

@login_required
def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            
            answer_formset = AnswerFormSet(request.POST, instance=question)
            if answer_formset.is_valid():
                answer_formset.save()
                return redirect('add_questions', quiz_id=quiz.id)
    else:
        question_form = QuestionForm()
        answer_formset = AnswerFormSet()

    return render(request, 'main/add_questions.html', {
        'quiz': quiz,
        'question_form': question_form,
        'answer_formset': answer_formset
    })

@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user == quiz.creator:
        quiz.delete()
    return redirect('quiz_list')

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
        session.finished_at = timezone.now()
        session.save()
        return redirect('quiz_result', session_id=session.id)

    question = questions[question_index]

    if request.method == 'POST':
        answer_id = request.POST.get('answer')
        if not answer_id:
            error = "Будь ласка, оберіть відповідь."
            return render(request, 'main/quiz_question.html', {
                'question': question,
                'session': session,
                'finished': False,
                'error': error
            })
        answer = get_object_or_404(Answer, id=int(answer_id))
        UserAnswer.objects.create(
            session=session,
            question=question,
            selected_answer=answer,
            is_correct=answer.is_correct
        )
        if answer.is_correct:
            session.score += 1
            session.save()
        return redirect('quiz_question', session_id=session.id, question_index=question_index+1)

    return render(request, 'main/quiz_question.html', {
        'question': question,
        'session': session,
        'finished': False
    })

@login_required
def quiz_result(request, session_id):
    session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    user_answers = UserAnswer.objects.filter(session=session)
    return render(request, 'main/quiz_result.html', {
        'session': session,
        'user_answers': user_answers
    })
