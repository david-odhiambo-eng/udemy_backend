from fastapi import APIRouter, status, Depends, HTTPException
from app.db.db_connections import get_db
from sqlalchemy.orm import Session
from app.db.topic_quiz_table import Question, TopicQuestion
from app.schemas.get_quiz import GetQuiz
from sqlalchemy import func

quiz_router = APIRouter(tags=["GET QUIZ ROUTE"])


@quiz_router.post("/questions", status_code=status.HTTP_200_OK)
def get_quiz(topic_names: GetQuiz, db: Session = Depends(get_db)):
    try:
        questions = (
            db.query(Question)
            .join(TopicQuestion, Question.question_id == TopicQuestion.question_id)
            .filter(TopicQuestion.topic_name.in_(topic_names.topic_names))
            .order_by(func.random())
            .limit(100)
            .all()
        )

        return questions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )
