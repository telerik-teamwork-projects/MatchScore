from fastapi import FastAPI
import uvicorn
from routers.user_router import router as user_router

app = FastAPI()
app.include_router(user_router, prefix='/users')

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)