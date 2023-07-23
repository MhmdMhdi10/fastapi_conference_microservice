from fastapi import FastAPI

from users_mgt import users_main
from conferences_mgt import conference_main

app = FastAPI()

app.mount("/auth", users_main.users_app)
app.mount("/conferences_mgt", conference_main.conference_app)
