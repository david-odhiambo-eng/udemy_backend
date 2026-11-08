from fastapi import FastAPI
from settings.load_env import SQLALCHEMY_URL
from app.db.db_connections import Base
from app.db.db_connections import engine
from app.routes.auth import auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.get_quiz import quiz_router
from app.routes.topic_quiz_route import topic_quiz_router

dev_mode = FastAPI(title="DEV MODE")

origins = ["http://localhost:55248", "http://192.168.100.6:8000"]

dev_mode.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@dev_mode.get("/")
def root():
    print(SQLALCHEMY_URL)
    return {"message": "Hello dev_mode developer"}


dev_mode.include_router(auth_router)
dev_mode.include_router(topic_quiz_router)
dev_mode.include_router(quiz_router)
Base.metadata.create_all(bind=engine)
