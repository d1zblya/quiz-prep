from src.schemes.schema_questions import QuestionSchema
from src.schemes.schema_user_answers import UserAnswerSchema
from src.bot.utils import get_question_text, get_final_text


def test_get_question_text():
    question = QuestionSchema(
        id=1,
        question="Сколько будет 2+2?",
        answer=4,
        doc_name="doc1",
        doc_point="point1"
    )

    result = get_question_text(question, 1)
    expected = "Вопрос номер 1\n\nСколько будет 2+2?"
    assert result == expected


def test_get_final_text():
    answers = [
        UserAnswerSchema(question_number=1, user_answer=4, correct_answer=4),
        UserAnswerSchema(question_number=2, user_answer=5, correct_answer=4),
    ]

    result = get_final_text(answers, correct_answers=1)

    expected = (
        "Всего вопросов: 2\n\nСтатистика:\n"
        "1. Ваш ответ: 4, Правильный: 4 ✅\n"
        "2. Ваш ответ: 5, Правильный: 4 ❌\n"
        "\nИтог: 1/2 правильных"
    )

    assert result == expected
