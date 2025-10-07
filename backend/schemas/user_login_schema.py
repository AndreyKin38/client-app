from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    id_client: int
    access_token: str


class UserCreateSchema(BaseModel):
    user_name: str
    password: str

