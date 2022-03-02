from typing import Optional, List

from fastapi import Depends, status, APIRouter, HTTPException, Response
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import schema, models
from .. import utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


# this is called endpoint
# to create new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.outschema)
def put_data(user: schema.createpost, db: Session = Depends(get_db),
             get_current_user: int = Depends(oauth2.get_current_user)):
    # u = models.product(id=user.id, Name=user.Name, Email=user.Email, Address=user.Address, is_active=user.is_active,
    #                    password=user.password, first_name=user.first_name)

    # # hashing of pasword:
    psw_hashing = utils.hasing(user.password)
    user.password = psw_hashing

    print("Current user that we logged in: ", get_current_user.id)

    # if we work on a real world project there is alote of field it may be 1000 or more
    # to add data to that field is just like above soo its very difficlut and time consuming
    # to that in a simple way we used this
    u = models.Post(owner_id=get_current_user.id, **user.dict())
    db.add(u)
    db.commit()
    db.refresh(u)

    # both return work are same
    return u
    # return {"data": u}


# to get all of the post from the database
@router.get("/", response_model=List[schema.Post_votes])
def get_data(db: Session = Depends(get_db),
             get_current_user: int = Depends(oauth2.get_current_user), Limit: int = 10, skip: int = 0,
             search: Optional[str] = ""):
    print("current User: ", get_current_user.id)
    print("Limit: ", Limit)

    # data = db.query(models.Post).filter(models.Post.Name.contains(search)).limit(Limit).offset(skip).all()

    # this logic return only those post which is created by that user
    # data = db.query(models.Post).filter(models.Post.owner_id == get_current_user.id).all()

    # join two table (post and vote) that we known how many time this post have been liked:
    # in sqlAlchemy by default join is (left outer join)
    result = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote,
                                                                                       models.Vote.post_id == models.Post.id,
                                                                                       isouter=True).group_by(
        models.Post.id).limit(Limit).offset(skip).all()

    print("Queery: ", result)

    return result


# with the help of this endpoint we get an indiviual post:
@router.get("/{id}", response_model=schema.Post_votes)
def get_data(id: int, db: Session = Depends(get_db),
             get_current_user: int = Depends(oauth2.get_current_user)):
    # e.g if we search id number 1 we get it directly but the all() continue his searching upto last
    # so that's way i used first() method when id found out it will stop searching
    # get_data = db.query(models.product).filter(models.product.id==id).all()
    get_data = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote,
                                                                                         models.Vote.post_id == models.Post.id,isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    print(get_data)
    if get_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your Post with id {id} are not found")
    return get_data


# with the help of this endpoint we delete specific post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                get_current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    post_query = post.first();

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your post with id {id} is not found")

    if post_query.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform request action")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# with the help of this endpoint we update specific post
@router.put("/{id}", response_model=schema.outschema)
def update_post(id: int, post_update: schema.update_schema, db: Session = Depends(get_db),
                get_current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your post with {id} is not found")

    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not Allowed to update any other post ")

    post_query.update(post_update.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
    # return {"Update:": post_query.first()}
