from jose import jwt, JWTError
from fastapi import HTTPException
from app.config import SECRET_KEY, ALGORITHM


def verify_jwt(token: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")