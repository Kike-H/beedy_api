from fastapi import FastAPI, responses
from src.routes.routes import *
app = FastAPI(
    title="Beedy API", 
    description="This the API for LMS Beedy",
    version="0.0.1"
)

app.include_router(users_routes)
app.include_router(files)

app.middleware('http')(catch_exception_middleware)

@app.get('/')
async def docs():
    ''' 
    Redirect to the documentation of Beedy API
    '''
    return responses.RedirectResponse('/docs')