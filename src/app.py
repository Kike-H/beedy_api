from fastapi import FastAPI, responses
from config.database import conn

app = FastAPI()

@app.get('/')
async def docs():
    ''' 
    Redirect to the documentation of Beedy API
    '''
    return responses.RedirectResponse('/docs')