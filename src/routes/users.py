from uuid import uuid4
from fastapi import APIRouter
from src.models.user import User
from src.config.database import conn
from src.schemas.users import users
from werkzeug.security import generate_password_hash

users_routes = APIRouter()

@users_routes.post('/users/register', response_model=User)
def create_user(user:User):
    '''This method saves a new user in to the database'''
    user.id = str(uuid4())
    user.password = generate_password_hash(user.password)
    conn.execute(users.insert().values(user.asdict()))
    return user

