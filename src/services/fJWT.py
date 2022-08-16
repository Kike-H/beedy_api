from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from fastapi import HTTPException

from dotenv import load_dotenv
import os 
load_dotenv()

def expire_date(days: int) -> str:
    return datetime.now() + timedelta(days)

def write_token(data:dict):
    return encode(payload={** data, "exp":expire_date(2)}, key=os.getenv("SECRETE"), algorithm="HS256")

def validate_token(token, output=False):
    try:
        if(output):
            return decode(token, key=os.getenv("SECRETE"), algorithms=["HS256"])
        decode(token, key=os.getenv("SECRETE"), algorithms=["HS256"])
    except exceptions.DecodeError:
        raise HTTPException(401, "Invalid token")
    except exceptions.ExpiredSignatureError:
        raise HTTPException(401, "Exppired token")