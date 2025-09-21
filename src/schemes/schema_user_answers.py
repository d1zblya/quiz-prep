from pydantic import BaseModel


class UserAnswerSchema(BaseModel):
    question_number: int
    user_answer: int
    correct_answer: int
