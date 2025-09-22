import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.services import service_questions
from src.exceptions.exception_questions import NotFounAllQuesions, ErrorRandomGeneratingQuestions
from src.schemes.schema_questions import QuestionSchema


def test_read_all_questions_success():
    fake_questions = [
        MagicMock(id=1, question="Q1", answer=1, doc_name="doc1", doc_point="point1"),
        MagicMock(id=2, question="Q2", answer=2, doc_name="doc2", doc_point="point2"),
    ]

    with patch("src.repositories.repository_questions.read_all_questions", return_value=fake_questions):
        session = MagicMock(spec=Session)
        result = service_questions.read_all_questions(session)

    assert len(result) == 2
    assert all(isinstance(q, QuestionSchema) for q in result)
    assert result[0].question == "Q1"


def test_read_all_questions_none():
    with patch("src.repositories.repository_questions.read_all_questions", return_value=None):
        session = MagicMock(spec=Session)
        with pytest.raises(NotFounAllQuesions):
            service_questions.read_all_questions(session)


def test_get_random_questions_success():
    fake_questions = [
        MagicMock(id=1, question="Q1", answer=1, doc_name="doc1", doc_point="point1"),
        MagicMock(id=2, question="Q2", answer=2, doc_name="doc2", doc_point="point2"),
        MagicMock(id=3, question="Q3", answer=3, doc_name="doc3", doc_point="point3"),
    ]

    with patch("src.repositories.repository_questions.read_all_questions", return_value=fake_questions):
        session = MagicMock(spec=Session)
        result = service_questions.get_random_questions(session, count=2)

    assert len(result) == 2
    assert all(isinstance(q, QuestionSchema) for q in result)


def test_get_random_questions_too_many():
    fake_questions = [
        MagicMock(id=1, question="Q1", answer=1, doc_name="doc1", doc_point="point1"),
    ]

    with patch("src.repositories.repository_questions.read_all_questions", return_value=fake_questions):
        session = MagicMock(spec=Session)
        with pytest.raises(ErrorRandomGeneratingQuestions):
            service_questions.get_random_questions(session, count=5)
