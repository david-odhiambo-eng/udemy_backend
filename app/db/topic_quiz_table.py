from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.db_connections import Base


class Topic(Base):
    __tablename__ = "topic"
    topic_id = Column(Integer, primary_key=True, index=True)
    topic_name = Column(String(30), nullable=False, unique=True)


class Question(Base):
    __tablename__ = "question"
    question_id = Column(Integer, primary_key=True, index=True)
    quiz = Column(String, nullable=False, unique=True)
    answer = Column(String, nullable=True, unique=False)
    key_word = Column(String, nullable=True, unique=False)
    topic = Column(String, nullable=False,unique=False)


class TopicQuestion(Base):
    __tablename__ = "topic_question"
    topic_name = Column(
        String,
        ForeignKey("topic.topic_name"),
        primary_key=True,
        index=True,
    )
    question_id = Column(
        Integer,
        ForeignKey("question.question_id"),
        primary_key=True,
        index=True,
    )
