from fastapi import APIRouter, HTTPException, Response, UploadFile, File
from os import makedirs, path, getcwd, rename, rmdir
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy.orm import Session
from sqlalchemy import desc
from types import NoneType
from typing import List

from src.models.file import FileIn, FileOut
from src.schemas.file import files
from src.config.database import conn, engine

files_routes = APIRouter()

ROOT_DIR = path.abspath(path.join(getcwd(), './files/'))

@files_routes.post('/upload/namecourse/{name_course}/idUser/{id_user}', response_model=FileOut, tags=['Files'], status_code=201)
async def upload_file(name_course:str, id_user:str, file_in: UploadFile = File(...)):
    '''This route add a new file to a course'''
    uri = ROOT_DIR + '/' + id_user + '/' + name_course + '/' + file_in.filename
    try:
        with open (uri, 'wb') as save_file:
            content = await file_in.read()
            save_file.write(content)
            save_file.close()
        new_id = conn.execute(files.insert().values(FileIn(name=file_in.filename, path=uri, idUser=id_user, nameCourse=name_course).asdict())).lastrowid
        return FileOut(id=new_id, name=file_in.filename, path=uri)
    except Exception as e:
        raise HTTPException(500, str(e))

@files_routes.get('/get/course/{name}', response_model=List[FileOut], tags=['Files'], status_code=200)
def get_file_by_name_course(name:str):
    '''This route  get all the files of a course'''
    response_files = conn.execute(files.select().where(files.c.nameCourse==name)).all()
    if(len(response_files) == 0):
        raise HTTPException(404, 'Not Found')
    return response_files

# TODO: make this route 
@files_routes.get('/get', response_model=FileOut, tags=['Files'], status_code=200)
def get_streaming_file(id: str = ""):
    '''This route get a streaming file'''
    # search = "%{}%".format(name)
    # with Session(engine) as s:
    #     response_courses = s.query(courses).filter(courses.c.name.like(search)).all()
    #     s.close()
    # if(len(response_courses) == 0):
    #     raise HTTPException(404, 'Not Found')
    # return response_courses

# TODO: make this route 
@files_routes.put('/get/update', response_model=FileOut, tags=['Files'], status_code=200)
def update_file(course_in: FileIn):
    '''This route update a file by id'''
    # uri = ROOT_DIR + '/' + course_in.idUser + '/' + course_in.name
    # course_old = conn.execute(courses.select().where(courses.c.id==course_in.id)).first()
    # if(type(course_old) == NoneType):
    #     raise HTTPException(404, 'Course not found')
    # try:
    #     rename(course_old.path, uri)
    #     conn.execute(courses.update().values(name=course_in.name, path=uri).where(courses.c.id==course_in.id))
    #     return CourseOut(id=course_old.id, name=course_in.name, path=uri)
    # except Exception as e:
    #     raise HTTPException(404, str(e))

# TODO: make this route 
@files_routes.delete('/delete/{id}', tags=['Files'], status_code=204)
def delete_file(id:str):
    '''This route delete a file by id'''
    # try:
    #     course = conn.execute(courses.select().where(courses.c.id==id)).first()
    #     rmdir(course.path)
    #     conn.execute(courses.delete().where(courses.c.id==id))
    #     return Response(status_code=HTTP_204_NO_CONTENT)
    # except Exception as e:
    #     raise HTTPException(404, str(e))
