from aiogram.dispatcher.filters.state import StatesGroup, State


class WeatherSub(StatesGroup):
    format = State()
    location = State()


class QuizStates(StatesGroup):
    quiz = State()

from telegram.models import Quiz, Question, Choice
history_quiz = Quiz.objects.create(title="Исторический квиз")
questions_data = [
    ("В каком году произошла Великая Французская революция?", [
        ("1789", True),
        ("1812", False),
        ("1905", False),
        ("1945", False)
    ]),
    ("Кто был первым президентом США?", [
        ("Джордж Вашингтон", True),
        ("Авраам Линкольн", False),
        ("Джон Ф. Кеннеди", False),
        ("Теодор Рузвельт", False)
    ]),
    ("Кто написал произведение 'Война и мир'?", [
        ("Лев Толстой", True),
        ("Федор Достоевский", False),
        ("Александр Пушкин", False),
        ("Иван Тургенев", False)
    ]),
]
for question_text, choices_with_correctness in questions_data:
    question = Question.objects.create(quiz=history_quiz, text=question_text)
    for choice_text, is_correct in choices_with_correctness:
        Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)