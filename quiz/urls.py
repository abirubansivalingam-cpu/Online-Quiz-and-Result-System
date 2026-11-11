from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("quiz/<int:quiz_id>/", views.quiz_detail, name="quiz_detail"),
    path("quiz/<int:quiz_id>/start/", views.start_quiz, name="start_quiz"),
    path("attempt/<int:attempt_id>/submit/", views.submit_quiz, name="submit_quiz"),
    path("result/<int:attempt_id>/", views.result_detail, name="result_detail"),
    path("results/", views.result_history, name="result_history"),
]
