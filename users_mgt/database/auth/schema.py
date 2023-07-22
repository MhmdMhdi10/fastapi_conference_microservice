from pydantic import BaseModel, BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Setting(BaseSettings):
    authjwt_secret_key: str = os.environ.get('SECRET_KEY')


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "username": "MM10",
                "password": "12345678",
            }
        }


class LoginModel(BaseModel):
    username: str
    password: str
