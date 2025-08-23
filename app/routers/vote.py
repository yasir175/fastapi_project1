from pyexpat import model
from typing import List, Optional
# from sentry_sdk import HttpTransport
from app import oauth2
from .. import schemas,models
from fastapi import Depends,HTTPException, Response,status,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router=APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def votes(vote:schemas.vote,db:Session=Depends(get_db),
          get_current_user:int=Depends(oauth2.get_current_user)):
    
    post_query=db.query(models.Post).filter(models.Post.id==vote.post_id)
    found_post=post_query.first()

    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {vote.post_id} does not exist.")


    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,
                                            models.Vote.user_id==get_current_user.id)
    found_vote=vote_query.first()
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user with id: {get_current_user.id} already voted on post with id: {vote.post_id}.")
        
        new_vote=models.Vote(user_id=get_current_user.id,post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return{"message":"vote added successfully"}
        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted the vote."}