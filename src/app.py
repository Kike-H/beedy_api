from fastapi import FastAPI, responses
from .middlewares.resolve import resolve
from src.routes.routes import *
from src.middlewares.middlewares import *

app = FastAPI(
    title="Beedy API", 
    description="This the API for LMS Beedy",
    version="0.1.2"
)

app.include_router(users_routes, prefix='/users')
app.include_router(courses_routes, prefix='/courses')
app.include_router(files_routes, prefix='/files')

app.middleware('http')(resolve)

@app.get('/', tags=['Docs'])
async def docs():
    ''' 
    Redirect to the documentation of Beedy API
    '''
    return responses.RedirectResponse('/docs')