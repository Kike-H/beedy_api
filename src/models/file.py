from typing import Optional
from pydantic import BaseModel

class FileBase(BaseModel):
    '''This model represent a base file'''
    id:Optional[int]
    name: str

class FileIn(FileBase):
    ''' This class represents the paramenters of new file '''
    idUser: str
    idCourse: str

    def asdict(self) -> dict:
        return {
            "idUser":self.idUser,
            "idCourse":self.idCourse,
            "name":self.name,
        }

class FileOut(FileBase):
    ''' This class represents a new course ''' 
    pass