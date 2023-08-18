from fastapi import FastAPI
from .routers import heroes


app = FastAPI()

app.include_router(router=heroes.router)


@app.on_event("startup")
def on_startup():
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("app starting up...")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
