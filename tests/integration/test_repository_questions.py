import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base, Question
from src.repositories import repository_questions


class TestRepositoryQuestions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def create_questions(self):
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
        self.session.add_all([q1, q2])
        self.session.commit()
        self.session.refresh(q1)
        self.session.refresh(q2)
        return [q1, q2]

    def test_read_all_questions_success(self):
        questions = self.create_questions()
        all_questions = repository_questions.read_all_questions(self.session)
        self.assertEqual(len(all_questions), len(questions))
        self.assertIsInstance(all_questions, list)
        self.assertTrue(all(isinstance(q, Question) for q in all_questions))
        self.assertEqual(all_questions[0].question, "1 + 1?")

    def test_read_all_questions_with_none_session(self):
        with self.assertRaises(AttributeError):
            repository_questions.read_all_questions(None)  # type: ignore

    def test_read_all_questions_with_invalid_session_str(self):
        with self.assertRaises(AttributeError):
            repository_questions.read_all_questions("not a session")  # type: ignore

    def test_read_all_questions_with_invalid_session_int(self):
        with self.assertRaises(AttributeError):
            repository_questions.read_all_questions(1)  # type: ignore

    def test_read_all_questions_empty_list(self):
        all_questions = repository_questions.read_all_questions(self.session)
        self.assertEqual(all_questions, [])

    def test_read_question_by_question_id_success(self):
        first_question = self.create_questions()[0]
        result = repository_questions.read_question_by_question_id(self.session, first_question.id)
        self.assertNotEqual(result, None)
        self.assertEqual(result.id, first_question.id)
        self.assertEqual(result.question, first_question.question)
        self.assertEqual(result.answer, first_question.answer)
        self.assertEqual(result.doc_name, first_question.doc_name)
        self.assertEqual(result.doc_point, first_question.doc_point)

    def test_read_question_by_question_id_with_not_exist_id(self):
        self.create_questions()
        result = repository_questions.read_question_by_question_id(self.session, 10 ** 6)
        self.assertEqual(result, None)

    def test_read_question_by_question_id_with_none_session(self):
        with self.assertRaises(AttributeError):
            repository_questions.read_question_by_question_id(None, 1)  # type: ignore

    def test_read_question_by_question_id_with_invalid_session_str(self):
        with self.assertRaises(AttributeError):
            repository_questions.read_question_by_question_id("not a session", 1)  # type: ignore

    def test_read_question_by_question_id_with_invalid_session_int(self):
        with self.assertRaises(AttributeError):
            repository_questions.read_question_by_question_id(1, 1)  # type: ignore

    def test_read_question_by_question_id_with_none_question_id(self):
        question = repository_questions.read_question_by_question_id(self.session, None)  # type: ignore
        self.assertIsNone(question)

    def test_read_question_by_question_id_with_invalid_question_id(self):
        question = repository_questions.read_question_by_question_id(
            self.session, "not a question id"  # type: ignore
        )
        self.assertIsNone(question)

    def test_read_question_by_question_id_none(self):
        result = repository_questions.read_question_by_question_id(self.session, 0)
        self.assertIsNone(result)
