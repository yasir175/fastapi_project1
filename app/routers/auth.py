from fastapi import Depends,HTTPException, Response,status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas,models,utils,oauth2
from ..database import get_db

router=APIRouter(
    tags=['authentication']
)

@router.get("/login")
def user_login(user_details:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    actual=db.query(models.Users).filter(models.Users.email==user_details.username).first()

    if not actual:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Input")
    
    if not utils.verify(user_details.password,actual.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Input")
    

    access_token=oauth2.create_access_token(data={"user_id":actual.id})

    return {"access_token":access_token,"token type":"bearer"}
