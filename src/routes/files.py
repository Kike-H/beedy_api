from werkzeug.security import check_password_hash
from os import getcwd, makedirs, path, rename, remove
from types import NoneType
from fastapi import APIRouter, File, UploadFile
from shutil import rmtree

from src.models.files import FileData
from src.config.database import conn
from src.models.folder import Folder
from src.schemas.users import users

files = APIRouter()

ROOT_DIR = path.abspath(path.join(getcwd(), './files/'))

@files.post('/files/create-new/folder', response_model=Folder, tags=['Folder'])
def create_new_folder(folder: Folder):
    uri = ROOT_DIR+'/'+folder.id+'-'+folder.name+'/'
    try:
        makedirs(uri)
        folder.path = uri
        return folder
    except:
        raise TypeError({"details":'this path already exists', "status_code": 400})

@files.put('/files/update/folder/{new_name}', response_model=Folder, tags=['Folder'])
def update_folder(new_name:str, folder: Folder):
    new_uri = ROOT_DIR+'/'+folder.id+'-'+new_name+'/'
    rename(folder.path, new_uri)
    folder.name = new_name
    folder.path = new_uri
    return folder

@files.delete('/files/remove/folder/', tags=['Folder'])
def remove_folder(folder:Folder):
    user = conn.execute(users.select().where(users.c.id==folder.id)).first()
    if(type(user) != NoneType and check_password_hash(user.password, folder.password)):
        rmtree(folder.path)
        return folder.path
    raise TypeError({"Details":'Cant delete the course', "status_code":400})

@files.post('/files/create-new/file-{id}-{folder}', response_model=FileData, tags=['Files'])
async def create_new_file(id:str, folder:str ,file: UploadFile = File(...)):
    file_data = FileData(id=id, folder=folder, name=file.filename)
    file_data.generatePath(ROOT_DIR+'/')
    with open (file_data.path, "wb") as file_saved:
        content = await file.read()
        file_saved.write(content)
        file_saved.close()
    return file_data
