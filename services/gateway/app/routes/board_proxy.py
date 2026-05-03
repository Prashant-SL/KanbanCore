from fastapi import APIRouter, Request, Response, HTTPException
import httpx

from app.config import BOARD_SERVICE, RATE_LIMIT
from app.rate_limit import limiter
from app.security import verify_jwt

router = APIRouter()


@router.api_route("/boards", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], tags=["Board Proxy"])
@router.api_route("/boards/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], tags=["Board Proxy"])
@router.api_route("/tasks", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], tags=["Board Proxy"])
@router.api_route("/tasks/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], tags=["Board Proxy"])
@limiter.limit(RATE_LIMIT)
async def board_proxy(request: Request, path: str = ""):

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

    headers = dict(request.headers)
    headers.pop("host", None)

    # Use the original request path to forward exactly what was requested
    forward_path = request.url.path
    url = f"{BOARD_SERVICE.rstrip('/')}{forward_path}"

    async with httpx.AsyncClient(timeout=60.0) as client:

        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            params=request.query_params,
            content=await request.body()
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers)
    )