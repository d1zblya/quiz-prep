from src.schemes.schema_questions import QuestionSchema
from src.schemes.schema_user_answers import UserAnswerSchema


def get_question_text(question: QuestionSchema, question_number: int) -> str:
    text = f"Вопрос номер {question_number}\n\n{question.question}"
    return text


def get_final_text(user_answers: list[UserAnswerSchema], correct_answers: int) -> str:
    total_questions = len(user_answers)

    text = f"Всего вопросов: {total_questions}\n\nСтатистика:\n"

    for ua in user_answers:
        is_correct = ua.user_answer == ua.correct_answer
        mark = "✅" if is_correct else "❌"
        text += (
            f"{ua.question_number}. Ваш ответ: {ua.user_answer}, "
            f"Правильный: {ua.correct_answer} {mark}\n"
        )

    text += f"\nИтог: {correct_answers}/{total_questions} правильных"
    return text
