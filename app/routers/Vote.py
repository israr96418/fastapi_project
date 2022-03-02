from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import database, schema, oauth2, models

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_for_user(vote: schema.vote, db: Session = Depends(database.get_db),
                  get_current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == get_current_user.id)

    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {get_current_user.id} has been already liked the post with {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=get_current_user.id)
        db.add(new_vote)
        db.commit()
        # db.refresh(new_vote)

        return {"message": "Your vote has been successfully added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Your post with id {vote.post_id} does't exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Your Post has been successfully unliked"}
