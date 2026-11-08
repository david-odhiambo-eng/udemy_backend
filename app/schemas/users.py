from pydantic import BaseModel, ConfigDict


class CreateUser(BaseModel):
    email: str
    player_name: str
    password: str


class CreateUserResponse(BaseModel):
    email: str
    player_name: str
    model_config = ConfigDict(from_attributes=True)


class LoginUser(BaseModel):
    email: str
    password: str

class LoginUserResponse(BaseModel):
    email: str
    player_name: str
    access_token: str
    token_type: str
