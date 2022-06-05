from fastapi import FastAPI, responses
from src.routes.routes import *
app = FastAPI()

app.include_router(users_routes)
app.include_router(files)

app.middleware('http')(catch_exception_middleware)

@app.get('/')
async def docs():
    ''' 
    Redirect to the documentation of Beedy API
    '''
    return responses.RedirectResponse('/docs')