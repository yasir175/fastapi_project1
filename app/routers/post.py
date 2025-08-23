from typing import List, Optional

from sqlalchemy import func
# from sentry_sdk import HttpTransport
from app import oauth2
from .. import schemas,models
from fastapi import Depends,HTTPException, Response,status,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router=APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user),
              limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    # print(posts)
    allposts=db.query(models.Post,func.count(models.Vote.post_id).label("Vote")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return [{"Post": post, "votes": votes} for post, votes in allposts]


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def createposts(post:schemas.PostBase,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)): 
    # type: ignore
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s,%s) RETURNING *""",
    #                (posts.title,posts.content,posts.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    # return {"data" :new_post}
    # print(get_current_user.email)
    new_post=models.Post(user_id=get_current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




@router.get("/{id}",response_model=schemas.PostOut)
def get_post_by_id(id:int,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s """, (id,))
    # target_post=cursor.fetchone()
    target_post=db.query(models.Post,func.count(models.Vote.post_id).label("Vote")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    
    if not target_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    post, votes = target_post 
    if post.user_id != get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform this action"
        )
    # print(target_post)
        
    return {"Post":post,"votes":votes}



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(id,))
    # index=cursor.fetchone()
    # conn.commit()
    target_post=db.query(models.Post).filter(models.Post.id==id)
    post_to_be_deleted = target_post.first()

    
    if post_to_be_deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    if post_to_be_deleted.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorized to performe this action")

    target_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.PostBase,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",
    #                (post.title,post.content,post.published,id))
    # updated_post=cursor.fetchone()
    # conn.commit()
    updated_post=db.query(models.Post).filter(models.Post.id==id)
    post_to_be_updated=updated_post.first()

    if post_to_be_updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    
    if post_to_be_updated.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to performe this action")

    updated_post.update(post.dict(),synchronize_session=False)
    db.commit()
    return updated_post.first()


