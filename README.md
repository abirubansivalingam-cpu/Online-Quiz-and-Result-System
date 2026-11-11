# Online Quiz and Result System

A beginner-friendly MCA mini project built with Python, Django, SQLite, HTML and CSS.

## Features
- Student registration, login and logout
- Quiz listing and instructions
- Multiple-choice quiz attempts
- Countdown timer with automatic submission when time expires
- Automatic scoring, percentage, pass/fail result
- Student result history
- Django admin for creating quizzes and questions

## Setup on Windows (Command Prompt)
1. Install Python 3.11+ from https://www.python.org/downloads/ and enable "Add Python to PATH".
2. Extract this ZIP to `C:\Users\YOUR_USERNAME\Downloads\online_quiz_result_system`.
3. Open Command Prompt and run:

```bat
cd %USERPROFILE%\Downloads\online_quiz_result_system
py -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe manage.py makemigrations quiz
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py createsuperuser
.venv\Scripts\python.exe manage.py seed_demo
.venv\Scripts\python.exe manage.py runserver
```

4. Open http://127.0.0.1:8000/
5. Admin: http://127.0.0.1:8000/admin/ (use the superuser you created)

## Demo student
Register your own student account at the website. The `seed_demo` command creates sample quizzes and questions, not a default user/password.

## Notes
- This is a local academic demo, not production-hardened. Set a secret key, DEBUG=False, secure cookies, HTTPS and proper deployment settings before public deployment.
- The browser timer improves usability, but server-side time checks are also applied.


## UI refresh
This package includes a dark navy and violet visual refresh for the existing QuizNest templates.
The update is CSS-first and preserves the existing Django views, URL names, forms, quiz timer,
automatic scoring and result-history flow. After replacing your project with this package,
restart the Django development server and hard-refresh the browser (Ctrl+F5).
