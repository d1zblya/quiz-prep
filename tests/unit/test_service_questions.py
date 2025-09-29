import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from src.exceptions.exception_questions import NotFounAllQuesions, ErrorRandomGeneratingQuestions
from src.schemes.schema_questions import QuestionSchema
from src.services import service_questions


class TestServiceQuestions(unittest.TestCase):
    def setUp(self):
        self.fake_one_questions = [
            MagicMock(id=1, question="Q1", answer=1, doc_name="doc1", doc_point="point1"),
        ]
        self.fake_two_questions = [
            MagicMock(id=1, question="Q1", answer=1, doc_name="doc1", doc_point="point1"),
            MagicMock(id=2, question="Q2", answer=2, doc_name="doc2", doc_point="point2"),
        ]
        self.fake_three_questions = [
            MagicMock(id=1, question="Q1", answer=1, doc_name="doc1", doc_point="point1"),
            MagicMock(id=2, question="Q2", answer=2, doc_name="doc2", doc_point="point2"),
            MagicMock(id=3, question="Q3", answer=3, doc_name="doc3", doc_point="point3"),
        ]

    def test_read_all_questions_success(self):
        with patch(
                "src.repositories.repository_questions.read_all_questions",
                return_value=self.fake_two_questions):
            session = MagicMock(spec=Session)
            result = service_questions.read_all_questions(session)

        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(q, QuestionSchema) for q in result))

    def test_read_all_questions_not_found(self):
        with patch("src.repositories.repository_questions.read_all_questions", return_value=None):
            session = MagicMock(spec=Session)
            with self.assertRaises(NotFounAllQuesions):
                service_questions.read_all_questions(session)

    def test_read_all_questions_with_empty_list(self):
        with patch("src.repositories.repository_questions.read_all_questions", return_value=[]):
            session = MagicMock(spec=Session)
            result = service_questions.read_all_questions(session)
        self.assertEqual(result, [])

    def test_get_random_questions_success(self):
        with patch(
                "src.repositories.repository_questions.read_all_questions",
                return_value=self.fake_three_questions):
            session = MagicMock(spec=Session)
            result = service_questions.get_random_questions(session, count=2)

        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(q, QuestionSchema) for q in result))

    def test_get_random_questions_unique(self):
        with patch(
                "src.repositories.repository_questions.read_all_questions",
                return_value=self.fake_three_questions):
            session = MagicMock(spec=Session)
            result = service_questions.get_random_questions(session, count=2)

        ids = [q.id for q in result]
        self.assertEqual(len(ids), len(result))

    def test_get_random_questions_equal_count(self):
        with patch(
                "src.repositories.repository_questions.read_all_questions",
                return_value=self.fake_three_questions):
            session = MagicMock(spec=Session)
            result = service_questions.get_random_questions(session, count=3)
        self.assertEqual(len(result), 3)

    def test_get_random_questions_too_many(self):
        with patch(
                "src.repositories.repository_questions.read_all_questions",
                return_value=self.fake_one_questions):
            session = MagicMock(spec=Session)
            with self.assertRaises(ErrorRandomGeneratingQuestions):
                service_questions.get_random_questions(session, count=5)
