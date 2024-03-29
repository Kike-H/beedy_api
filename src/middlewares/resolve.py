from starlette.requests import Request
from starlette.responses import Response
import json


async def resolve(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        try:
            code =  e.args[0]['status_code']
        except:
            code = 500
        return Response(
            content=json.dumps(e.args[0]), 
            status_code=code, 
            media_type="application/json"
        )


