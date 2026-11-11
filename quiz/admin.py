from django.contrib import admin
from .models import Quiz, Question, Attempt

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "duration_minutes", "pass_mark", "is_published", "question_count")
    list_filter = ("is_published",)
    search_fields = ("title",)
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "text", "correct_option")
    list_filter = ("quiz",)
    search_fields = ("text",)

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("student", "quiz", "score", "total_questions", "percentage", "passed", "completed_at")
    list_filter = ("quiz", "passed")
    readonly_fields = ("student", "quiz", "score", "total_questions", "percentage", "passed", "started_at", "completed_at")
