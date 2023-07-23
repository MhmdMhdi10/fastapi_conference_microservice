import inspect
import re

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from fastapi_jwt_auth import AuthJWT

from database.database import Base, engine
from conferences.conference_routes import conference_router


Base.metadata.create_all(bind=engine)

conference_app = FastAPI()

conference_app.include_router(conference_router)
