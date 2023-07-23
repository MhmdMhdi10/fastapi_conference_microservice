from fastapi import APIRouter, status, Depends
from database.database import SessionLocal, engine
from fastapi.exceptions import HTTPException

from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

from database.conferences.models import Conferences
from database.conferences.schema import ConferenceModel

import requests


conference_router = APIRouter(
    prefix="/conferences",
    tags=["conferences"]
)

session = SessionLocal(bind=engine)


def validate_token(token):
    resp = requests.get("http://localhost:8000/validate", headers={"Authorization": f"Bearer {token}"})
    return resp.json()["valid"]


@conference_router.post("/conference", status_code=status.HTTP_201_CREATED)
async def create_conference(conference: ConferenceModel, token: str = Depends(validate_token)):
    """
    ## create new conference
    this requires the following:
    - title: str
    - description: str
    - start_time: datetime = datetime.now()
    - end_time: Optional[datetime]
    - Capacity: int
    """
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user = requests.get("http://localhost:8000/users/me", headers={"Authorization": f"Bearer {token}"})

    new_conference = Conferences(
        title=conference.title,
        description=conference.description,
        start_time=conference.start_time,
        end_time=conference.end_time,
        Capacity=conference.Capacity
    )

    new_conference.user_username = user

    session.add(new_conference)

    session.commit()

    response = {
        "id": new_conference.id,
        "title": new_conference.title,
        "description": new_conference.description,
        "start_time": new_conference.start_time,
        "end_time": new_conference.end_time,
    }

    return jsonable_encoder(response)


@conference_router.get("/conferences", status_code=status.HTTP_200_OK)
async def list_all_conferences(token: str = Depends(validate_token)):
    """
        ## listing all conferences
    """
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    conferences = session.query(Conferences).all()

    return jsonable_encoder(conferences)


@conference_router.put("/conferences/{conference_id}", status_code=status.HTTP_200_OK)
async def update_conference(conference_id: int, conference: ConferenceModel, token: str = Depends(validate_token)):
    """
        ## Updating a conference
        this updates a conference requires the following list:
        - id : int
        - title : str
        - description : str
        - start_time: datetime
        - end_time: datetime
    """

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    try:
        conference_to_update = session.query(Conferences).filter(Conferences.id == conference_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conference not found")

    all_conferences = session.query(Conferences).all()

    for con in all_conferences:
        if con.id == conference.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="A conference with this id already exists")

    conference_to_update.id = conference.id
    conference_to_update.title = conference.title
    conference_to_update.description = conference.description
    conference_to_update.start_time = conference.start_time
    conference_to_update.end_time = conference.end_time

    session.commit()

    response = {
        "title": conference_to_update.title,
        "description": conference_to_update.description,
        "start_time": conference_to_update.start_time,
        "end_time": conference_to_update.end_time,
    }

    return jsonable_encoder(response)


@conference_router.delete("/conferences/{conference_id}", status_code=status.HTTP_200_OK)
async def delete_conference(conference_id: int, token: str = Depends(validate_token)):
    """
        ## deleting a conference
        this deletes a conference
    """

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    conference_to_delete = session.query(Conferences).filter(Conferences.id == conference_id).first()

    try:
        session.delete(conference_to_delete)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conference not found")
    session.commit()
    return conference_to_delete
