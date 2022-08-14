from typing import Optional
from pydantic import BaseModel
from src.schemas.users import userRole
class User(BaseModel):
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

class UserRegister(User):
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

class UserSaved(BaseModel):
    id: str
    status: str
    status_code: int
    message = "New user registered"

class LoginUser(BaseModel):
    email: str
    password: str