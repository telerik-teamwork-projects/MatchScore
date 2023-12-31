from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from starlette.staticfiles import StaticFiles

from routers.users_router import router as users_router
from routers.matches_router import router as matches_router
from routers.tournaments_router import router as tournaments_router
from routers.players_router import router as players_router
from routers.requests_router import router as requests_router
from routers.search_router import router as search_router
from routers.weather_router import router as weather_router

app = FastAPI()
app.include_router(users_router, prefix='/users')
app.include_router(matches_router, prefix='/matches')
app.include_router(tournaments_router, prefix='/tournaments')
app.include_router(players_router, prefix="/players")
app.include_router(requests_router, prefix="/requests")
app.include_router(search_router, prefix="/search")
app.include_router(weather_router, prefix='/weather')

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
