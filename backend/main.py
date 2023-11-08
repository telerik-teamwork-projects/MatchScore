from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from starlette.staticfiles import StaticFiles

from routers.user_router import router as user_router
from routers.matches_router import router as matches_router

app = FastAPI()
app.include_router(user_router, prefix='/users')
app.include_router(matches_router, prefix='/matches')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory="media"), name="media")

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
