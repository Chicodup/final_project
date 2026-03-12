from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from .models import Quiz, Question, Answer, QuizSession, UserAnswer
from .forms import QuizForm, QuestionForm, AnswerForm

AnswerFormSet = inlineformset_factory(
    Question, Answer, form=AnswerForm, extra=4, can_delete=True
)

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
            return redirect('edit_quiz', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'main/create_quiz.html', {
        'form': form,
        'title': "Створити вікторину",
        'is_edit': False
    })

@login_required
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user != quiz.creator and not request.user.is_staff:
        return redirect('quiz_list')

    QuestionFormSet = inlineformset_factory(
        Quiz, Question, form=QuestionForm, extra=0, can_delete=True
    )

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, instance=quiz)
        formset = QuestionFormSet(request.POST, instance=quiz)
        if quiz_form.is_valid() and formset.is_valid():
            quiz_form.save()
            formset.save()
            return redirect('edit_quiz', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm(instance=quiz)
        formset = QuestionFormSet(instance=quiz)

    return render(request, 'main/edit_quiz.html', {
        'quiz': quiz,
        'quiz_form': quiz_form,
        'formset': formset,
        'title': "Редагувати вікторину",
        'is_edit': True
    })

@login_required
def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
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
def edit_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user != quiz.creator and not request.user.is_staff:
        return redirect('quiz_list')

    question = get_object_or_404(Question, id=question_id, quiz=quiz)

    if request.method == 'POST':
        q_form = QuestionForm(request.POST, instance=question)
        a_formset = AnswerFormSet(request.POST, instance=question)
        if q_form.is_valid() and a_formset.is_valid():
            q_form.save()
            a_formset.save()
            return redirect('edit_quiz', quiz_id=quiz.id)
    else:
        q_form = QuestionForm(instance=question)
        a_formset = AnswerFormSet(instance=question)

    return render(request, 'main/edit_question.html', {
        'quiz': quiz,
        'q_form': q_form,
        'a_formset': a_formset,
        'question': question
    })

@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user == quiz.creator or request.user.is_staff:
        quiz.delete()
    return redirect('quiz_list')

@login_required
def quiz_results_admin(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user != quiz.creator and not request.user.is_staff:
        return redirect('quiz_list')

    sessions = QuizSession.objects.filter(quiz=quiz, completed=True).order_by('-started_at')
    all_results = []

    for session in sessions:
        user_answers = UserAnswer.objects.filter(session=session)
        all_results.append({
            'session': session,
            'user_answers': user_answers
        })

    return render(request, 'main/quiz_results_admin.html', {
        'quiz': quiz,
        'all_results': all_results
    })

@login_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user != quiz.creator and not request.user.is_staff:
        return redirect('quiz_list')

    sessions = QuizSession.objects.filter(quiz=quiz, completed=True).order_by('-score')
    return render(request, 'main/quiz_results.html', {
        'quiz': quiz,
        'sessions': sessions
    })

def enter_name(request, quiz_id):
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        if player_name:
            request.session['player_name'] = player_name
            return redirect('start_quiz', quiz_id=quiz_id)
    return render(request, 'main/name.html', {'quiz_id': quiz_id})

def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if quiz.deadline and timezone.now() > quiz.deadline:
        return render(request, 'main/quiz_closed.html', {'quiz': quiz})

    if not request.session.session_key:
        request.session.create()

    session = QuizSession.objects.create(
        quiz=quiz,
        session_key=request.session.session_key,
        player_name=request.session.get('player_name', 'Гравець')
    )

    return redirect('quiz_question', session_id=session.id, question_index=0)

def quiz_question(request, session_id, question_index):
    session = get_object_or_404(QuizSession, id=session_id, session_key=request.session.session_key)
    questions = list(session.quiz.question_set.all())
    total_questions = len(questions)

    if question_index >= total_questions:
        session.completed = True
        session.finished_at = timezone.now()
        session.save()
        return redirect('quiz_result', session_id=session.id)

    question = questions[question_index]

    if request.method == 'POST':
        answer_id = request.POST.get('answer')
        answer = None
        is_correct = False

        if answer_id:
            answer = get_object_or_404(Answer, id=int(answer_id))
            is_correct = answer.is_correct
            if is_correct:
                session.score += 1
                session.save()

        UserAnswer.objects.create(
            session=session,
            question=question,
            selected_answer=answer,
            is_correct=is_correct
        )

        return redirect('quiz_question', session_id=session.id, question_index=question_index + 1)

    return render(request, 'main/quiz_question.html', {
        'session': session,
        'question': question,
        'question_index': question_index + 1,
        'total_questions': total_questions
    })

def quiz_result(request, session_id):
    session = get_object_or_404(QuizSession, id=session_id, session_key=request.session.session_key)
    user_answers = UserAnswer.objects.filter(session=session)
    return render(request, 'main/quiz_result.html', {
        'session': session,
        'user_answers': user_answers
    })