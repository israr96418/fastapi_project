# with the help of 'python-jose[cryptography]" this library i will create jwt and also verify it
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from . import schema, models, database
# from . config import setting

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
print("oauth_schema", oauth2_schema)

# to create jwt we eill have 3 things
# secrete key
# algorithms
# expiration times

SECRET_KEY = "20a1893f2be0ac96dd61d0faa0137cf3dcf626ae12a09d960d7939d94199c2eb"
# HS256  is encryptio algroithms
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# SECRET_KEY = {setting.secret_key}
# # HS256  is encryptio algroithms
# ALGORITHM = {setting.algorithms}
# ACCESS_TOKEN_EXPIRE_MINUTES = {setting.access_token_expiration_time}




# with the help of this function i will create a token

def create_access_token(data: dict):
    print("ajsjdhfasjdhfajsfh")
    # ye o data he jo me token ke payload me lana chahta ho
    to_encode = data.copy()
    print("token_encoded", to_encode)
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire_time})
    print("token_encoded_after_added a time", to_encode)

    # now we create jwt token
    json_web_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print("Token_data", json_web_token)

    return json_web_token


def verify_acces_token(token: str, credentials_acceptions):

    try:
        print("calling by getUser")
        print("Token_verificaion", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Token_decoded", payload)
        id: str = payload.get("user_id")
        print("user_id_ofthe_token",id)

        if id is None:
            raise credentials_acceptions
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_acceptions

    return token_data


# it will gave the current user that we logged in
def get_current_user(token: str = Depends(oauth2_schema), db:Session=Depends(database.get_db)):
    credentials_acceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail=f"Could not validate credentials",
                                           headers={"WWW-Authenticate": "bearer"})
    token=verify_acces_token(token, credentials_acceptions)
    curent_user=db.query(models.User).filter(models.User.id==token.id).first()

    return curent_user
