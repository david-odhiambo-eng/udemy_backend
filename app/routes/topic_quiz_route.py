from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db_connections import get_db
from app.db.topic_quiz_table import Topic, Question, TopicQuestion
from app.schemas.topic_quiz import CreateTopic, CreateQuiz, QuestionResponse

topic_quiz_router = APIRouter(tags=["TOPICS AND QUESTIONS"])


@topic_quiz_router.post(
    "/topic_quiz", status_code=status.HTTP_201_CREATED, response_model=QuestionResponse
)
def create_topic_and_quiz(
    topic_data: CreateTopic, quiz_data: CreateQuiz, db: Session = Depends(get_db)
):
    try:
        topic = (
            db.query(Topic).filter(Topic.topic_name == topic_data.topic_name).first()
        )
        # check if topic exist

        # if not, create topic
        if not topic:
            topic = Topic(topic_name=topic_data.topic_name)
            db.add(topic)
            db.flush()
        # if yes, proceed to create a question
        question = Question(
            quiz=quiz_data.quiz,
            answer=quiz_data.answer,
            key_word=quiz_data.key_word,
            topic=quiz_data.topic,
        )
        db.add(question)
        db.flush()

        # finally create TopicQuestion table
        topic_quiz = TopicQuestion(
            topic_name=topic.topic_name, question_id=question.question_id
        )
        db.add(topic_quiz)
        db.commit()
        return QuestionResponse(
            quiz_id=question.question_id, topic_name=topic.topic_name
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            detail=f"{str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
