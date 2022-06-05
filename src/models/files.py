from importlib.resources import path
from typing import Optional
from pydantic import BaseModel

class FileData(BaseModel):
    '''
    This class rerpsent a folder with the next values:

    - id 
    - name
    - folder
    - password (Optional)
    - path (Optional) 

    '''

    id: str
    name: str
    folder: str
    password: Optional[str]
    path: Optional[str]

    def generatePath(self, before_path:str='./'):
        '''
        This method generate a path of the file with the atributes
        * before_path is optional 
        '''
        self.path = before_path+self.id+'-'+self.folder+'/'+self.name

    def asdict(self) -> dict:
        '''This method return the user object like a dictionary'''
        return {
            "id": self.id,
            "name": self.name, 
            "folder": self.folder,
            "password": self.password,
            "path": self.path
        }