from pydantic import BaseModel


class GetQuiz(BaseModel):
    topic_names: list[str]
