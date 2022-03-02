from fastapi import Depends, APIRouter, HTTPException, status
# from .. import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, utils, models, oauth2
from .. import schema

router = APIRouter(
    tags=["Authenticaion"]
)


# most important things:
# from hash passwrd we cannot convert into orginal password so we convert the passwr that we enter into hash
# then we compare with hash passwrd that is already stored in the databse

@router.post('/login', response_model=schema.Token)
def user_login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print("useridkk")
    user = db.query(models.User).filter(models.User.Email == user_credential.username).first()
    print("userid", user)
    # {
    #     "username":"isrardawar485@gmail.com",
    #     "password":"khan1234"
    # }
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials(Email)")

    if not utils.verify_password_of_user(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials(Password)")

    #   create jsw token:
    #   return token

    # and After that i handle the token
    # return {"access":"token"}

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # print("khan")
    return {"access_token": access_token, "token_type": "bearer"}
