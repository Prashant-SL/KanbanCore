from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from sqlalchemy import text
from app.db import SessionLocal, engine, Base
from app.routes import board_routes, column_routes, task_routes

app = FastAPI()


Base.metadata.create_all(bind=engine)
app.include_router(board_routes.router)
app.include_router(column_routes.router)
app.include_router(task_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://kanbancore-gateway-service.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],  # Fixed: changed ["GET, POST"] to ["*"] to allow OPTIONS preflight requests
    allow_headers=["*"],
)

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