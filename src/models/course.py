from typing import Optional
from unicodedata import name
from pydantic import BaseModel

class CourseBase(BaseModel):
    ''' This class represents a course'''
    id: Optional[int]
    path: Optional[str]
    name: str

class CourseIn(CourseBase):
    ''' This class represents the paramenters of new course '''
    idUser: str

    def asdict(self) -> dict:
        return {
            "idUser":self.idUser,
            "name":self.name,
            "path":self.path
        }

class CourseOut(CourseBase):
    ''' This class represents a new course ''' 
    path:str