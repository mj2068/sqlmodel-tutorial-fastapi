from fastapi import FastAPI
from .routers import heroes, teams


app = FastAPI()

app.include_router(router=heroes.router, tags=["Hero"])
app.include_router(router=teams.router, tags=["Team"])


@app.on_event("startup")
def on_startup():
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("app starting up...")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
