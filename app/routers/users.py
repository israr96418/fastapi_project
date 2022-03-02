from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session

from .. import oauth2
from .. import schema, models, utils
from ..database import get_db

router = APIRouter(
    prefix="/new",
    tags=["User"]
)


# Endpoint for User Registration:
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.outschema_for_post)
def new_user(post: schema.inschema_for_userProf, db: Session = Depends(get_db)):

    # print("current_user_that we logged in", current_user.Email)

    # hash the user password when user Enter the password
    # hashing means to convert the original password into other formate, by that hacker cannot known the orignal password
    psw_hashing = utils.hasing(post.password)
    post.password = psw_hashing

    data = models.User(**post.dict())
    db.add(data)
    db.commit()
    db.refresh(data)

    return data


@router.get("/{id}", response_model=schema.outschema_for_userprof)
def new_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    print("current_user",current_user.Email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your new user with id {id} is not found")

    return user
