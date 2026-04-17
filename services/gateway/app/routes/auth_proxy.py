from fastapi import APIRouter, Request, Response
import httpx
from app.rate_limit import limiter


from app.config import AUTH_SERVICE

router = APIRouter()

@router.api_route("/auth/{path:path}", methods=["GET","POST","PUT","DELETE","OPTIONS"], tags=["Auth Proxy"])
async def auth_proxy(path: str, request: Request):

    headers = dict(request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:

        response = await client.request(
            request.method,
            f"{AUTH_SERVICE}/{path}",
            headers=headers,
            content=await request.body()
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers)
    )