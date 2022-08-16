from fastapi import APIRouter, HTTPException, Response, UploadFile, File, Header, Request
from os import path, getcwd, remove, rename
from starlette.status import HTTP_204_NO_CONTENT
from fastapi.responses import Response
from types import NoneType
from typing import List

from src.models.file import FileIn, FileOut
from src.schemas.file import files
from src.schemas.courses import courses
from src.config.database import conn

from src.middlewares.jwt import VerifyToken

files_routes = APIRouter(route_class=VerifyToken)

ROOT_DIR = path.abspath(path.join(getcwd(), './files/'))

PORTION_SIZE = 1024 * 1024

@files_routes.post('/upload/idcourse/{id_course}', response_model=FileOut, tags=['Files'], status_code=201)
async def upload_file(request:Request, id_course:str, file_in: UploadFile = File(...)):
    '''This route add a new file to a course'''
    course = conn.execute(courses.select().where(courses.c.id==id_course)).first()
    role = request.state.role
    uri = course.path + '/' + file_in.filename
    if(role == 'tutor'):
        try:
            with open (uri, 'wb') as save_file:
                content = await file_in.read()
                save_file.write(content)
                save_file.close()
            new_id = conn.execute(files.insert().values(FileIn(name=file_in.filename, idUser=course.idUser, idCourse=course.id).asdict())).lastrowid
            return FileOut(id=new_id, name=file_in.filename, path=uri)
        except Exception as e:
            raise HTTPException(500, str(e))

@files_routes.get('/get/course/{id}', response_model=List[FileOut], tags=['Files'], status_code=200)
def get_file_by_id_course(request:Request, id:str):
    role = request.state.role
    if(role == 'student'):
        '''This route  get all the files of a course'''
        response_files = conn.execute(files.select().where(files.c.idCourse==id)).all()
        if(len(response_files) == 0):
            raise HTTPException(404, 'Not Found')
        return response_files
    else : raise HTTPException(401, 'Invalid role')

@files_routes.get('/get/streaming/video/{id}', tags=['Files'], status_code=200)
def get_streaming_file(request:Request, id:str, apiKey:str = '', range: str = Header(None)):
    role = request.state.role
    if(role == 'student'):
        '''This route get a streaming file'''
        start, end = range.replace("bytes=", "").split("-")
        start = int(start)
        end = int(end) if end else int(start + PORTION_SIZE)

        file = conn.execute(files.select().where(files.c.id==id)).first()
        course = conn.execute(courses.select().where(courses.c.id==file.idCourse)).first()
        uri = course.path + '/' +file.name
        with open(uri, 'rb') as video:
            video.seek(start)
            data = video.read(start + end)
            size_video = str(path.getsize(uri))

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

@files_routes.put('/get/update/{id}/name', response_model=FileOut, tags=['Files'], status_code=200)
def update_file(id: str, name:str =""):
    '''This route update the video name'''
    file = conn.execute(files.select().where(files.c.id==id)).first()
    course = conn.execute(courses.select().where(courses.c.id==file.idCourse)).first()
    uri_old = course.path + '/' + file.name
    uri_new = course.path + '/' + name
    if(type(file) == NoneType):
        raise HTTPException(404, 'Course not found')
    if(name == ""):
        raise HTTPException(404, 'No new file name')
    try:
        rename(uri_old, uri_new)
        conn.execute(files.update().values(name=name).where(files.c.id==id))
        return FileOut(id=file.id, name=name)
    except Exception as e:
        raise HTTPException(404, str(e))

@files_routes.delete('/delete/{id}', tags=['Files'], status_code=204)
def delete_file(id:str):
    '''This route delete a file by id'''
    try:
        file = conn.execute(files.select().where(files.c.id==id)).first()
        course = conn.execute(courses.select().where(courses.c.id==file.idCourse)).first()
        uri = course.path + '/' + file.name
        remove(uri)
        conn.execute(files.delete().where(files.c.id==id))
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(404, str(e))
