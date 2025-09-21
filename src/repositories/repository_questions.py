from sqlalchemy.orm import Session

from src.database.models import Question


def read_all_questions(session: Session) -> list[Question]:
    questions = session.query(Question).all()
    return questions  # type: ignore


def read_question_by_question_id(session: Session, question_id: int) -> Question:
    question = session.query(Question).filter_by(id=question_id).first()
    return question  # type: ignore
