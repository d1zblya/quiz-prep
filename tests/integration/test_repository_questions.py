import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base, Question
from src.repositories import repository_questions


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def questions(session):
    q1 = Question(
        question="1 + 1?",
        answer=2,
        doc_name="doc1",
        doc_point="point1"
    )
    q2 = Question(
        question="2 + 2?",
        answer=4,
        doc_name="doc2",
        doc_point="point2"
    )
    session.add_all([q1, q2])
    session.commit()
    session.refresh(q1)
    session.refresh(q2)
    return [q1, q2]


def test_read_all_questions_success(session, questions):
    all_questions = repository_questions.read_all_questions(session)
    assert len(all_questions) == 2
    assert all(isinstance(q, Question) for q in all_questions)
    assert all_questions[0].question == "1 + 1?"


def test_read_all_questions_none(session):
    questions = repository_questions.read_all_questions(session)
    assert len(questions) == 0


def test_read_question_by_question_id_success(session, questions):
    first_question = questions[0]
    result = repository_questions.read_question_by_question_id(session, first_question.id)
    assert result is not None
    assert result.id == first_question.id
    assert result.question == first_question.question
    assert result.answer == first_question.answer
    assert result.doc_name == first_question.doc_name
    assert result.doc_point == first_question.doc_point


def test_read_question_by_question_id_none(session):
    result = repository_questions.read_question_by_question_id(session, 0)
    assert result is None
