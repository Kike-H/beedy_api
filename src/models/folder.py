from typing import Optional
from pydantic import BaseModel

class Folder(BaseModel):
    '''
    This class rerpsent a folder with the next values:

    - id 
    - name
    - password (Optional)
    - path (Optional)

    '''
    id: str
    name: str
    password: Optional[str]
    path: Optional[str]

    def asdict(self) -> dict:
        '''This method return the user object like a dictionary'''
        return {
            "id": self.id, 
            "name": self.name, 
            "password": self.password,
            "path": self.path
        }