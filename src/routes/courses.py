from fastapi import APIRouter, HTTPException
from os import makedirs, path, getcwd
from typing import List

from src.models.course import CourseIn, CourseOut
from src.schemas.courses import courses
from src.config.database import conn

courses_routes = APIRouter()

ROOT_DIR = path.abspath(path.join(getcwd(), './files/'))

@courses_routes.post('/add', response_model=CourseOut, tags=['courses'], status_code=201)
def addNewCourse(course_in: CourseIn):
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
def getCoursesByUser(id:str):
    '''This route  get all the courses of a user'''
    response_courses = conn.execute(courses.select().where(courses.c.idUser==id)).all()
    if(len(response_courses) == 0):
        raise HTTPException(404, 'Not Found')
    return response_courses
