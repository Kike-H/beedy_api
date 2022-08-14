import datetime
from sqlalchemy import Table, Column, DateTime
from sqlalchemy.sql.sqltypes import String, Integer
from src.config.database import meta, engine

'''
This schema create if not exits the table users
'''

courses = Table(
    'courses',
    meta, 
    Column('id', Integer, primary_key=True),
    Column('idUser', String(255), nullable=False),
    Column('name', String(255), nullable=False),
    Column('path', String(255), nullable=False),
    Column('creationDate', DateTime, default=datetime.datetime.utcnow)
)

meta.create_all(engine)

