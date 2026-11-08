from pydantic import BaseModel, ConfigDict

class CreateTopic(BaseModel):
    topic_name: str


class CreateQuiz(BaseModel):
    quiz: str
    answer: str | None = None
    key_word: str | None = None
    topic: str


class QuestionResponse(BaseModel):
    quiz_id: int
    topic_name: str
    model_config = ConfigDict(from_attributes=True) 