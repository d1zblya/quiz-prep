import random

from loguru import logger
from sqlalchemy.orm import Session

from src.exceptions.exception_questions import NotFounAllQuesions, ErrorRandomGeneratingQuestions
from src.repositories import repository_questions
from src.schemes.schema_questions import QuestionSchema


def read_all_questions(session: Session) -> list[QuestionSchema]:
    questions = repository_questions.read_all_questions(session)
    if questions is None:
        msg = "Questions not found"
        logger.error(msg)
        raise NotFounAllQuesions(msg)
    question_schemas = [QuestionSchema.model_validate(q) for q in questions]
    return question_schemas


def get_random_questions(session: Session, count: int) -> list[QuestionSchema]:
    try:
        questions = read_all_questions(session)
        return random.sample(questions, count)
    except Exception as e:
        msg = f"Error generating questions: {e}"
        logger.error(msg)
        raise ErrorRandomGeneratingQuestions(msg)
