from fastapi import FastAPI
from app.routers.auth import router as register
from app.db.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(register)

