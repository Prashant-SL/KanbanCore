from fastapi import FastAPI
from sqlalchemy import text
from app.db import SessionLocal, engine, Base
from app.routes import board_routes, column_routes, task_routes

app = FastAPI()


Base.metadata.create_all(bind=engine)
app.include_router(board_routes.router)
app.include_router(column_routes.router)
app.include_router(task_routes.router)

@app.get("/healthcheck/board")
def read_root():
    return { "message": "Welcome to Board Service" }

@app.get("/db-health")
def getDb():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1"))
        value = result.scalar_one()
        return {"db_response": value}
    finally:
        db.close()