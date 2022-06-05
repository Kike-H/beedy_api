from uuid import uuid4
from types import NoneType
from fastapi import APIRouter
from werkzeug.security import generate_password_hash, check_password_hash

from src.models.user import User
from src.schemas.users import users
from src.config.database import conn

users_routes = APIRouter()

@users_routes.post('/users/register', response_model=User)
def create_user(user:User):
    '''This method saves a new user in to the database'''
    user.id = str(uuid4())
    user.password = generate_password_hash(user.password)
    try:
        conn.execute(users.insert().values(user.asdict()))
    except:
        raise TypeError({"Error":'This user alredy exits', "status_code":500})
    return user

@users_routes.get('/users/{email}/{password}', response_model=User)
def login_user(email:str, password:str):
    '''This path return a user if the credentials are correct'''
    user = conn.execute(users.select().where(users.c.email==email)).first()
    print(type(user))
    if(type(user) != NoneType and check_password_hash(user.password, password)):
        return user
    raise TypeError({"Error":'The creditals are wrong', "status_code":500})


