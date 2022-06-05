from fastapi import APIRouter

files = APIRouter()

@files.post('/files/create-new/{folder}')
def create_new_folder(folder:str):
    return (folder)

