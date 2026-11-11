from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import StudentRegistrationForm
from .models import Attempt, Quiz

def home(request):
    quizzes = Quiz.objects.filter(is_published=True).prefetch_related("questions")[:6]
    return render(request, "quiz/home.html", {"quizzes": quizzes})

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your student account has been created.")
            return redirect("dashboard")
    else:
        form = StudentRegistrationForm()
    return render(request, "quiz/register.html", {"form": form})

@login_required
def dashboard(request):
    quizzes = Quiz.objects.filter(is_published=True).prefetch_related("questions")
    attempts = Attempt.objects.filter(student=request.user, completed_at__isnull=False)[:5]
    return render(request, "quiz/dashboard.html", {"quizzes": quizzes, "attempts": attempts})

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    if quiz.question_count == 0:
        messages.warning(request, "This quiz has no questions yet.")
    return render(request, "quiz/quiz_detail.html", {"quiz": quiz})

@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    if request.method != "POST":
        return redirect("quiz_detail", quiz_id=quiz.id)
    if not quiz.questions.exists():
        messages.error(request, "This quiz is not ready yet.")
        return redirect("quiz_detail", quiz_id=quiz.id)
    attempt = Attempt.objects.create(
        student=request.user, quiz=quiz, total_questions=quiz.questions.count(),
        started_at=timezone.now()
    )
    return render(request, "quiz/take_quiz.html", {"quiz": quiz, "attempt": attempt, "questions": quiz.questions.all()})

@login_required
def submit_quiz(request, attempt_id):
    attempt = get_object_or_404(Attempt, id=attempt_id, student=request.user)
    if attempt.completed_at:
        return redirect("result_detail", attempt_id=attempt.id)
    if request.method != "POST":
        return redirect("dashboard")
    quiz = attempt.quiz
    questions = list(quiz.questions.all())
    elapsed = (timezone.now() - attempt.started_at).total_seconds()
    # Server-side time guard: allow a small 15-second submission buffer.
    if elapsed > quiz.duration_minutes * 60 + 15:
        messages.info(request, "The quiz time had expired; your submitted answers were evaluated.")
    score = 0
    for question in questions:
        answer = request.POST.get(f"question_{question.id}", "")
        if answer == question.correct_option:
            score += 1
    total = len(questions)
    percentage = round((score / total) * 100, 2) if total else 0
    attempt.score = score
    attempt.total_questions = total
    attempt.percentage = percentage
    attempt.passed = percentage >= quiz.pass_mark
    attempt.completed_at = timezone.now()
    attempt.save()
    return redirect("result_detail", attempt_id=attempt.id)

@login_required
def result_detail(request, attempt_id):
    attempt = get_object_or_404(Attempt, id=attempt_id, student=request.user, completed_at__isnull=False)
    return render(request, "quiz/result_detail.html", {"attempt": attempt})

@login_required
def result_history(request):
    attempts = Attempt.objects.filter(student=request.user, completed_at__isnull=False)
    return render(request, "quiz/result_history.html", {"attempts": attempts})
