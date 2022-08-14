from uuid import uuid4
from types import NoneType
from fastapi import APIRouter, HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

from src.models.user import User, UserLogin, UserRegister, UserSaved
from src.schemas.users import users
from src.config.database import conn

users_routes = APIRouter()

@users_routes.post('/users/register', response_model= UserSaved , tags=['Users'])
def create_user(newUser:UserRegister):
    '''This method saves a new user in to the database'''
    newUser.id = str(uuid4())
    newUser.password = generate_password_hash(newUser.password)
    try:
        conn.execute(users.insert().values(newUser.asdict()))
    except:
        raise HTTPException(500, 'This user already exists')
    return UserSaved(id=newUser.id, status="OK", status_code=200)

@users_routes.post('/users/login', response_model=User, tags=['Users'])
def login_user(userCredentials: UserLogin):
    '''This path return a user if the credentials are correct'''
    user = conn.execute(users.select().where(users.c.email==userCredentials.email)).first()
    if(type(user) != NoneType and check_password_hash(user.password, userCredentials.password)):
        return user
    raise HTTPException(500, 'The creditals are wrong')


