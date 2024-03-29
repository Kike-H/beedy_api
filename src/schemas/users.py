import enum
from sqlalchemy import  Enum, Table, Column
from sqlalchemy.sql.sqltypes import String
from src.config.database import meta, engine

'''
This schema create if not exits the table users
'''

class userRole(enum.Enum):
    student = "student"
    tutor = "tutor"

users = Table(
    'users',
    meta, 
    Column('id', String(255), nullable=False, unique= True, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('email', String(255), unique=True ,nullable=False),
    Column('password', String(255) ,nullable=False),
    Column('role', Enum(userRole) ,nullable=False),
)

meta.create_all(engine)

