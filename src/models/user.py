from typing import Optional
from pydantic import BaseModel
from src.schemas.users import userRole
class UserBase(BaseModel):
    '''
    This class rerpsent a user with the next values:

    - id (Optional)
    - name 
    - email

    '''
    id: Optional[str]
    name: str
    email: str
    role: userRole

class UserIn(UserBase):
    '''This class represents a new user to save '''
    password: str

    def asdict(self) -> dict:
        '''This method return the user object like a dictionary'''
        return {
            "id": self.id, 
            "name": self.name, 
            "email": self.email, 
            "password": self.password,
            "role": self.role
        }

class UserOut(BaseModel):
    id: str
    status: str
    status_code: int
    message = "New user registered"

class UserLogin(BaseModel):
    email: str
    password: str
    token: Optional[str]