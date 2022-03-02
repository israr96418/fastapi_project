from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.types import conint


# check the validation of the data through the pydantic model
# whether the data coming from the user is valid or not:
# means our pydantic model is according to the field of our database table


# INSCHEMA Means the data that user send to us
class validate_data(BaseModel):
    id: int
    Name: str
    Email: str
    Address: str
    is_active: bool = True
    password: str
    last_name: str

    # Behaviour of pydantic can be controlled via the Config class on a model or a pydantic dataclass
    # or provide configuration to pydantic
    class config:
        # it tell pydantic model to read the data even if it is not dictionary it may be object
        orm_mode: True


class createpost(validate_data):
    pass


class update_schema(BaseModel):
    Name: str
    Email: str

    # Behaviour of pydantic can be controlled via the Config class on a model or a pydantic dataclass
    # or provide configuration to pydantic
    class Config:
        # it tell pydantic model to read the data even if it is not dictionary it may be object
        orm_mode: True


class inschema_for_userProf(BaseModel):
    Name: str
    experience: str
    # EmailStr are used to check email string validation
    Email: EmailStr
    # Email:str
    password: str

    class Config:
        orm_mode = True


class outschema_for_userprof(BaseModel):
    id: int
    experience: str
    Name: str
    created_at: datetime

    class Config:
        orm_mode = True


# OUTSCHEMA Means that we send back response to the user
class outschema(BaseModel):
    id: int
    Name: str
    Email: str
    owner_id: int

    # Owner_info: outschema_for_userprof

    # post_created at: datetime

    class Config:
        orm_mode = True

class Post_votes(BaseModel):
    Post: outschema
    vote:int

    class Config:
        orm_mode = True

class user_Authenticaion(BaseModel):
    Email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# OutSchema for post when we created new_post
class outschema_for_post(BaseModel):
    id: int
    experience: str
    Name: str
    created_at: datetime

    class Config:
        orm_mode = True


class vote(BaseModel):
    post_id: int
    dir : conint(le= 1)
