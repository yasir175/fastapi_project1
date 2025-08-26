from fastapi import FastAPI
from app import models
from app.database import engine
from .routers import post,user,auth,vote
from .config import setting
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
origins=["*"]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# my_posts=[{"title":"post 1" ,"content":"content of post 1","id":1},{"title":"post 2" ,"content":"content of post 2","id":2}]

# def find_index(id):
#     for i,p in enumerate(my_posts):
#         if p['id']==id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    try:
        result = db.execute("SELECT 1").scalar()
        return {"database_connection": "successful" if result == 1 else "failed"}
    except Exception as e:
        return {"database_connection": "failed", "error": str(e)}


