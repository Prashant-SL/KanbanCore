from fastapi import APIRouter, Request, Response
import httpx
from app.rate_limit import limiter


from app.config import AUTH_SERVICE

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET","POST"], tags=["Auth Proxy"])
async def auth_proxy(path: str, request: Request):

    async with httpx.AsyncClient() as client:

        response = await client.request(
            request.method,
            f"{AUTH_SERVICE}/auth/{path}",
            headers=dict(request.headers),
            content=await request.body()
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=response.headers
    )