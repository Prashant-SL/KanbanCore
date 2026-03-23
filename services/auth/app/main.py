from fastapi import FastAPI
from sqlalchemy import text
from app.db import SessionLocal, engine, Base
from app.models import user_model
from app.routes import auth_routes

app = FastAPI()


Base.metadata.create_all(bind=engine)
app.include_router(auth_routes.router)

@app.get("/healthcheck/auth")
def read_root():
    return { "message": "Welcome to Auth Service" }

@app.get("/db-health")
def getDb():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1"))
        value = result.scalar_one()
        return {"db_response": value}
    finally:
        db.close()