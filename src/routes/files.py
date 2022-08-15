from fastapi import APIRouter, HTTPException, Response, UploadFile, File, Header
from os import path, getcwd, remove, rename
from starlette.status import HTTP_204_NO_CONTENT
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
from types import NoneType
from typing import List

from src.models.file import FileIn, FileOut
from src.schemas.file import files
from src.schemas.courses import courses
from src.config.database import conn, engine

files_routes = APIRouter()

ROOT_DIR = path.abspath(path.join(getcwd(), './files/'))

PORTION_SIZE = 1024 * 1024

@files_routes.post('/upload/namecourse/{idCourse}', response_model=FileOut, tags=['Files'], status_code=201)
async def upload_file(id_course:str, file_in: UploadFile = File(...)):
    '''This route add a new file to a course'''
    course = conn.execute(courses.select().where(courses.c.id==id_course)).first()
    uri = course.path + '/' + file_in.filename
    try:
        with open (uri, 'wb') as save_file:
            content = await file_in.read()
            save_file.write(content)
            save_file.close()
        new_id = conn.execute(files.insert().values(FileIn(name=file_in.filename, path=uri, idUser=course.idUser, nameCourse=course.name).asdict())).lastrowid
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

@files_routes.get('/get/streaming/video/{id}', tags=['Files'], status_code=200)
def get_streaming_file(id:str, range: str = Header(None)):
    '''This route get a streaming file'''
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else int(start + PORTION_SIZE)
    file = conn.execute(files.select().where(files.c.id==id)).first()
    with open(file.path, 'rb') as video:
        video.seek(start)
        data = video.read(start + end)
        size_video = str(path.getsize(file.path))

        headers = {
            "Content-Range": f'bytes {str(start)}-{str(end)}/{size_video}',
            "Accept-Ranges": "bytes"
        }
        return Response(
            content=data,
            status_code=206,
            headers=headers,
            media_type="video/mp4"
        )

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

@files_routes.delete('/delete/{id}', tags=['Files'], status_code=204)
def delete_file(id:str):
    '''This route delete a file by id'''
    try:
        file = conn.execute(files.select().where(files.c.id==id)).first()
        remove(file.path)
        conn.execute(files.delete().where(files.c.id==id))
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(404, str(e))
