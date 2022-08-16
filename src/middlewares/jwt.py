from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from src.services.fJWT import validate_token

class VerifyToken(APIRoute):
    def get_route_handler(self):
        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            token = ""
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except:
                try:
                    token = str(request.url).split("apiKey=")[1]
                except:
                    raise HTTPException(401, 'No Autorization')
            user = validate_token(token, output=True)
            role = user['role']
            id = user['id']

            if validate_token != None:
                request.state.role = role
                request.state.id = id
                return await original_route(request)
            else:
                return validate_token
        return verify_token_middleware
