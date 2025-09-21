from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.orm import Session

from src.bot.states.questionnaire import Questionnaire
from src.bot.utils import get_question_text, get_final_text
from src.schemes.schema_questions import QuestionSchema
from src.schemes.schema_user_answers import UserAnswerSchema
from src.services import service_questions

router = Router()


async def send_question(message: Message, state: FSMContext):
    data = await state.get_data()
    questions: list[QuestionSchema] = data.get("questions")
    current_question: int = data.get("current_question")
    correct_answers: int = data.get("correct_answers")
    count_questions: int = data.get("count_questions")

    if current_question < count_questions:
        question: QuestionSchema = questions[current_question]
        text = get_question_text(question=question, question_number=current_question + 1)
        await message.answer(text)
        await state.set_state(Questionnaire.waiting_answer)
    else:
        user_answers: list[UserAnswerSchema] = data.get("user_answers")
        text = get_final_text(user_answers=user_answers, correct_answers=correct_answers)
        await message.answer(text)
        await state.clear()


@router.callback_query(F.data.startswith("questions:"))
async def start_questionnaire(callback: CallbackQuery, state: FSMContext, session: Session):
    await callback.message.delete()
    count = int(callback.data.split(":")[1])
    questions = service_questions.get_random_questions(session=session, count=count)

    await state.update_data(
        questions=questions,
        current_question=0,
        correct_answers=0,
        count_questions=len(questions),
        user_answers=[],
    )
    await send_question(callback.message, state)


@router.message(Questionnaire.waiting_answer, F.text)
async def check_answer(message: Message, state: FSMContext):
    try:
        user_answer = int(message.text.strip())
    except ValueError:
        await message.answer("Введите вариант ответа числом!")
        return

    data = await state.get_data()
    questions: list[QuestionSchema] = data.get("questions")
    current_question: int = data.get("current_question")
    correct_answers: int = data.get("correct_answers")
    user_answers: list[UserAnswerSchema] = data.get("user_answers")

    correct_answer = int(questions[current_question].answer)

    user_answer_schema = UserAnswerSchema(
        question_number=current_question + 1,
        user_answer=user_answer,
        correct_answer=correct_answer
    )

    if user_answer == correct_answer:
        correct_answers += 1

    user_answers.append(user_answer_schema)

    await state.update_data(
        current_question=current_question + 1,
        user_answers=user_answers,
        correct_answers=correct_answers
    )

    await send_question(message, state)
