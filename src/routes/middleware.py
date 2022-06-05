from starlette.requests import Request
from starlette.responses import Response
import json

async def catch_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return Response(content=json.dumps(e.args), status_code=e.args[0]['status_code'], media_type="application/json")
