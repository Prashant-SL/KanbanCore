from fastapi import APIRouter, Request, Response, HTTPException
import httpx

from app.config import BOARD_SERVICE
from app.rate_limit import limiter
from app.security import verify_jwt

router = APIRouter()


@router.api_route("/{path:path}", methods=["GET", "POST"], tags=["Board Proxy"])
@limiter.limit("100/minute")
async def board_proxy(path: str, request: Request):

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        scheme, token = auth_header.split()
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")

    verify_jwt(token)

    async with httpx.AsyncClient() as client:

            response = await client.request(
            method=request.method,
            url=f"{BOARD_SERVICE}/{path}",
            headers=dict(request.headers),
            params=request.query_params,
            content=await request.body()
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers)
    )