import unittest

from src.bot.utils import get_question_text, get_final_text
from src.schemes.schema_questions import QuestionSchema
from src.schemes.schema_user_answers import UserAnswerSchema


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.question = QuestionSchema(
            id=1,
            question="Сколько будет 2+2?",
            answer=4,
            doc_name="doc1",
            doc_point="point1"
        )
        self.answers = [
            UserAnswerSchema(question_number=1, user_answer=4, correct_answer=4),
            UserAnswerSchema(question_number=2, user_answer=5, correct_answer=4),
        ]

    def test_get_question_text_success(self):
        result = get_question_text(self.question, 1)
        expected = "Вопрос номер 1\n\nСколько будет 2+2?"
        self.assertEqual(result, expected)

    def test_get_question_text_with_empty_text_question(self):
        empty_question = QuestionSchema(
            id=2, question="", answer=4, doc_name="doc1", doc_point="point1"
        )
        result = get_question_text(empty_question, 1)
        self.assertEqual(result, "Вопрос номер 1\n\n")

    def test_get_question_text_with_question_number_none(self):
        with self.assertRaises(TypeError):
            get_question_text(self.question, None)  # type: ignore

    def test_get_question_text_with_question_none(self):
        with self.assertRaises(AttributeError):
            get_question_text(None, 1)  # type: ignore

    def test_get_question_text_with_bad_question_scheme(self):
        with self.assertRaises(AttributeError):
            get_question_text({"foo": "bar"}, 1)  # type: ignore

    def test_get_final_text_success(self):
        result = get_final_text(self.answers, 1)

        expected = (
            "Всего вопросов: 2\n\nСтатистика:\n"
            "1. Ваш ответ: 4, Правильный: 4 ✅\n"
            "2. Ваш ответ: 5, Правильный: 4 ❌\n"
            "\nИтог: 1/2 правильных"
        )

        self.assertEqual(result, expected)

    def test_get_final_text_with_correct_answers_none(self):
        with self.assertRaises(TypeError):
            get_final_text(self.answers, None)  # type: ignore

    def test_get_final_text_with_user_answers_none(self):
        with self.assertRaises(TypeError):
            get_final_text(None, 1)  # type: ignore

    def test_get_final_text_with_bad_answer_scheme(self):
        with self.assertRaises(AttributeError):
            get_final_text({"foo": "bar"}, 1)  # type: ignore

