from typing import Optional
from pydantic import BaseModel
from src.schemas.users import userRole
class User(BaseModel):
    '''
    This class rerpsent a user with the next values:

    - id (Optional)
    - name 
    - email
    - password

    '''
    id: Optional[str]
    name: str
    email: str
    password: str
    role: userRole

    def asdict(self) -> dict:
        '''This method return the user object like a dictionary'''
        return {
            "id": self.id, 
            "name": self.name, 
            "email": self.email, 
            "password": self.password,
            "role": self.role
        }