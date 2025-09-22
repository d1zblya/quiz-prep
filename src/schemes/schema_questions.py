from pydantic import BaseModel, ConfigDict, Field


class QuestionSchema(BaseModel):
    id: int | None = Field(None)
    question: str
    answer: int
    doc_name: str
    doc_point: str

    model_config = ConfigDict(from_attributes=True)
