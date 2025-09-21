from pydantic import BaseModel, ConfigDict


class QuestionSchema(BaseModel):
    id: int
    question: str
    answer: int
    doc_name: str
    doc_point: str

    model_config = ConfigDict(from_attributes=True)
