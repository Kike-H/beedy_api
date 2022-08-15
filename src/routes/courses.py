from unicodedata import name
from fastapi import APIRouter, HTTPException
from os import makedirs, path, getcwd, rename
from sqlalchemy.orm import Session
from sqlalchemy import desc
from types import NoneType
from typing import List

from src.models.course import CourseIn, CourseOut
from src.schemas.courses import courses
from src.config.database import conn, engine

courses_routes = APIRouter()

ROOT_DIR = path.abspath(path.join(getcwd(), './files/'))

@courses_routes.post('/add', response_model=CourseOut, tags=['courses'], status_code=201)
def add_new_course(course_in: CourseIn):
    '''This route add a new course'''
    uri = ROOT_DIR + '/' + course_in.idUser + '/' + course_in.name
    try:
        makedirs(uri)
        course_in.path = uri
        new_id = conn.execute(courses.insert().values(course_in.asdict())).lastrowid
        return CourseOut(id=new_id, name=course_in.name, path=uri)
    except Exception as e:
        raise HTTPException(500, str(e))

@courses_routes.get('/get/{id}', response_model=List[CourseOut], tags=['courses'], status_code=200)
def get_courses_by_user(id:str):
    '''This route  get all the courses of a user'''
    response_courses = conn.execute(courses.select().where(courses.c.idUser==id)).all()
    if(len(response_courses) == 0):
        raise HTTPException(404, 'Not Found')
    return response_courses

@courses_routes.get('/get', response_model=List[CourseOut], tags=['courses'], status_code=200)
def get_courses_by_name(name: str = ""):
    '''This route  get all the courses by name'''
    search = "%{}%".format(name)
    with Session(engine) as s:
        response_courses = s.query(courses).filter(courses.c.name.like(search)).all()
        s.close()
    if(len(response_courses) == 0):
        raise HTTPException(404, 'Not Found')
    return response_courses

@courses_routes.get('get/last', response_model=List[CourseOut], tags=['courses'], status_code=200)
def get_courses_by_date():
    '''This route  get the last 5 courses'''
    with Session(engine) as s:
        response_courses = s.query(courses).order_by(desc(courses.c.creationDate)).limit(5).all()
        s.close()
    return response_courses

@courses_routes.put('get/update', response_model=CourseOut, tags=['courses'], status_code=200)
def update_course(course_in: CourseIn):
    '''This route update a course by id'''
    uri = ROOT_DIR + '/' + course_in.idUser + '/' + course_in.name
    course_old = conn.execute(courses.select().where(courses.c.id==course_in.id)).first()
    if(type(course_old) == NoneType):
        raise HTTPException(404, 'Course not found')
    rename(course_old.path, uri)
    conn.execute(courses.update().values(name=course_in.name, path=uri).where(courses.c.id==course_in.id))
    return CourseOut(id=course_old.id, name=course_in.name, path=uri)

