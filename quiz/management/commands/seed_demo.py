from django.core.management.base import BaseCommand
from quiz.models import Quiz, Question

SAMPLE_QUIZZES = [
    ("Python Basics", "Test your knowledge of Python fundamentals.", 5, 40, [
        ("Which keyword defines a function in Python?", "func", "def", "function", "method", "B"),
        ("Which data type stores key-value pairs?", "list", "tuple", "dictionary", "set", "C"),
        ("What is the result of 2 ** 3?", "5", "6", "8", "9", "C"),
        ("Which symbol starts a single-line comment in Python?", "//", "#", "/*", "--", "B"),
        ("Which collection is ordered and mutable?", "tuple", "list", "frozenset", "string", "B"),
    ]),
    ("Web Technology", "A short quiz on HTML, CSS and web basics.", 5, 40, [
        ("What does HTML stand for?", "HyperText Markup Language", "HighText Machine Language", "Hyper Tool Multi Language", "Home Tool Markup Language", "A"),
        ("Which HTML tag creates a hyperlink?", "<link>", "<a>", "<href>", "<url>", "B"),
        ("Which CSS property changes text color?", "font-style", "background", "color", "text-weight", "C"),
        ("Which HTTP method is commonly used to retrieve a page?", "POST", "DELETE", "GET", "PATCH", "C"),
        ("Which language adds interactivity in a browser?", "SQL", "JavaScript", "C", "Bash", "B"),
    ]),
]

class Command(BaseCommand):
    help = "Create sample quizzes and multiple-choice questions."

    def handle(self, *args, **options):
        for title, description, duration, pass_mark, questions in SAMPLE_QUIZZES:
            quiz, created = Quiz.objects.get_or_create(
                title=title,
                defaults={"description": description, "duration_minutes": duration, "pass_mark": pass_mark, "is_published": True},
            )
            if created:
                for text, a, b, c, d, correct in questions:
                    Question.objects.create(quiz=quiz, text=text, option_a=a, option_b=b, option_c=c, option_d=d, correct_option=correct)
                self.stdout.write(self.style.SUCCESS(f"Created sample quiz: {title}"))
            else:
                self.stdout.write(f"Already exists, skipped: {title}")
        self.stdout.write(self.style.SUCCESS("Demo quiz setup complete."))
