from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

@app.get('/is_auth')
async def is_auth():
    return Response(status_code=401)
