from fastapi import FastAPI, responses

app = FastAPI()

@app.get('/')
async def docs():
    return responses.RedirectResponse('/docs')