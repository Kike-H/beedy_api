from fastapi import FastAPI, responses
from src.routes.users import users_routes

app = FastAPI()

app.include_router(users_routes)

@app.get('/')
async def docs():
    ''' 
    Redirect to the documentation of Beedy API
    '''
    return responses.RedirectResponse('/docs')