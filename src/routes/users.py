import email
from uuid import uuid4
from types import NoneType
from fastapi import APIRouter, HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

from src.models.user import UserLoginIn, UserLoginOut, UserIn, UserLoginToken, UserOut
from src.schemas.users import users
from src.config.database import conn
from src.services.fJWT import write_token

users_routes = APIRouter()

@users_routes.post('/register', response_model= UserOut , tags=['Users'], status_code=201)
def create_user(newUser:UserIn):
    '''This method saves a new user in to the database'''
    newUser.id = str(uuid4())
    newUser.password = generate_password_hash(newUser.password)
    try:
        conn.execute(users.insert().values(newUser.asdict()))
    except:
        raise HTTPException(500, 'This user already exists')
    return UserOut(id=newUser.id, status="OK", status_code=200)

@users_routes.post('/login', response_model=UserLoginOut, tags=['Users'], status_code=202)
def login_user(userCredentials: UserLoginIn):
    '''This path return a user if the credentials are correct'''
    user = conn.execute(users.select().where(users.c.email==userCredentials.email)).first()
    if(type(user) != NoneType and check_password_hash(user.password, userCredentials.password)):
        user_token = UserLoginToken(id=user.id, role=str(user.role.value))
        token = str(write_token(user_token.asdict()))
        return UserLoginOut(token=token)
    raise HTTPException(500, 'The creditals are wrong')


