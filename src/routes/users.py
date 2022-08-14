from uuid import uuid4
from types import NoneType
from fastapi import APIRouter, HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

from src.models.user import User, UserRegister
from src.schemas.users import users
from src.config.database import conn

users_routes = APIRouter()

@users_routes.post('/users/register', response_model= UserRegister , tags=['Users'])
def create_user(user:User):
    '''This method saves a new user in to the database'''
    user.id = str(uuid4())
    user.password = generate_password_hash(user.password)
    try:
        conn.execute(users.insert().values(user.asdict()))
    except:
        raise HTTPException(500, 'This user already exists')
    return UserRegister(id=user.id, status="OK", status_code=200)

@users_routes.get('/users/{email}/{password}', response_model=User, tags=['Users'])
def login_user(email:str, password:str):
    '''This path return a user if the credentials are correct'''
    user = conn.execute(users.select().where(users.c.email==email)).first()
    if(type(user) != NoneType and check_password_hash(user.password, password)):
        return user
    raise TypeError({"error":'The creditals are wrong', "status_code":500})


