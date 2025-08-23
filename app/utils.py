from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verify(input_password,actual_password):
    return pwd_context.verify(input_password,actual_password)