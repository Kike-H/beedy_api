from typing import Optional
from pydantic import BaseModel

class FileBase(BaseModel):
    '''This model represent a base file'''
    id:Optional[int]
    path:Optional[str]
    name: str

class FileIn(FileBase):
    ''' This class represents the paramenters of new file '''
    idUser: str
    nameCourse: str
    idCourse: str

    def asdict(self) -> dict:
        return {
            "idUser":self.idUser,
            "idCourse":self.idCourse,
            "nameCourse":self.nameCourse,
            "name":self.name,
            "path":self.path
        }

class FileOut(FileBase):
    ''' This class represents a new course ''' 
    path:str