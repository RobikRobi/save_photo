from fastapi import FastAPI
from db import Base, engine
from router import app as router

app = FastAPI()
app.include_router(router)

@app.get("/init")
def create_db():
    Base.metadata.create_all(bind=engine)
    return {"msg": "db created!"}
