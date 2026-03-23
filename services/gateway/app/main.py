from fastapi import FastAPI, Request, Response, HTTPException
import httpx
from app.routes import auth_proxy, board_proxy

from app.config import AUTH_SERVICE, BOARD_SERVICE
from app.security import verify_jwt
from app.rate_limit import limiter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev
        # "https://abc.com", # production frontend
    ],
    allow_credentials=True,
    allow_methods=["GET, POST"],
    allow_headers=["*"],
)

app.include_router(auth_proxy.router)
app.include_router(board_proxy.router)