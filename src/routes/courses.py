from fastapi import APIRouter, HTTPException, Response, Request
from os import makedirs, path, getcwd, rename, rmdir
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import desc
from types import NoneType
from typing import List

from src.models.course import CourseIn, CourseOut
from src.schemas.courses import courses
from src.config.database import conn, engine
from src.middlewares.jwt import VerifyToken

courses_routes = APIRouter(route_class=VerifyToken)

ROOT_DIR = path.abspath(path.join(getcwd(), './files/'))

@courses_routes.post('/add', response_model=CourseOut, tags=['Courses'], status_code=201)
def add_new_course(course_in: CourseIn, request:Request):
    '''This route add a new course'''
    role = request.state.role
    id_user = request.state.id
    if(role == 'tutor'):
        uri = ROOT_DIR + '/' + id_user + '/' + course_in.name
        try:
            makedirs(uri)
            course_in.path = uri
            course_in.idUser = id_user
            new_id = conn.execute(courses.insert().values(course_in.asdict())).lastrowid
            return CourseOut(id=new_id, name=course_in.name, path=uri)
        except Exception as e:
            raise HTTPException(500, str(e))
    else: 
        raise HTTPException(401, 'Not User Authorization')

@courses_routes.get('/get', response_model=List[CourseOut], tags=['Courses'], status_code=200)
def get_courses_by_user(request: Request):
    '''This route  get all the courses of a user'''
    id_user = request.state.id
    response_courses = conn.execute(courses.select().where(courses.c.idUser==id_user)).all()
    if(len(response_courses) == 0):
        raise HTTPException(404, 'Not Found')
    return response_courses

@courses_routes.get('/get', response_model=List[CourseOut], tags=['Courses'], status_code=200)
def get_courses_by_name(name: str = ""):
    '''This route  get all the courses by name'''
    search = "%{}%".format(name)
    with Session(engine) as s:
        response_courses = s.query(courses).filter(courses.c.name.like(search)).all()
        s.close()
    if(len(response_courses) == 0):
        raise HTTPException(404, 'Not Found')
    return response_courses

@courses_routes.get('/get/last/', response_model=List[CourseOut], tags=['Courses'], status_code=200)
def get_courses_by_date():
    '''This route  get the last 5 courses'''
    with Session(engine) as s:
        response_courses = s.query(courses).order_by(desc(courses.c.creationDate)).limit(5).all()
        s.close()
    return response_courses

@courses_routes.put('/get/update/', response_model=CourseOut, tags=['Courses'], status_code=200)
def update_course(request: Request, id:str, name: str = ""):
    '''This route update a course by id'''
    course_old = conn.execute(courses.select().where(courses.c.id==id)).first()
    uri = ROOT_DIR + '/' + course_old.idUser + '/' + name
    role = request.state.role
    if(role == 'tutor'):
        if(type(course_old) == NoneType):
            raise HTTPException(404, 'Course not found')
        try:
            rename(course_old.path, uri)
            conn.execute(courses.update().values(name=name, path=uri).where(courses.c.id==id))
            return CourseOut(id=course_old.id, name=name, path=uri)
        except Exception as e:
            raise HTTPException(404, str(e))
    else :
            raise HTTPException(401, 'Not User Authorization')

@courses_routes.delete('/delete/{id}', tags=['Courses'], status_code=204)
def delete_course(request: Request, id:str):
    '''This route delete a course by id'''
    role = request.state.role
    if(role == 'tutor'):
        try:
            course = conn.execute(courses.select().where(courses.c.id==id)).first()
            rmdir(course.path)
            conn.execute(courses.delete().where(courses.c.id==id))
            return Response(status_code=HTTP_204_NO_CONTENT)
        except Exception as e:
            raise HTTPException(404, str(e))