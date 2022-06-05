from fastapi import APIRouter
from os import getcwd, makedirs, path, remove

from src.models.folder import Folder

files = APIRouter()

ROOT_DIR = path.abspath(path.join(getcwd(), './files/'))

@files.post('/files/create-new/folder', response_model=Folder)
def create_new_folder(folder: Folder):
    uri = ROOT_DIR+'/'+folder.id+'-'+folder.name+'/'
    try:
        makedirs(uri)
        folder.path = uri
        return folder
    except:
        raise TypeError({"details":'this path already exists', "status_code": 400})

