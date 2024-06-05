from datetime import datetime, timedelta

from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from core.config import env

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verification_password(input_password, hashed_password) -> bool:
    return pwd_context.verify(input_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    """
    :param data: {"sub":user[id]}
    :return:
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, env('SECRET_KEY'), algorithm=env('ALGORITHM'))


def decode_jwt_user_id(token: str) -> int | JSONResponse:
    try:
        payload = jwt.decode(token, env('SECRET_KEY'), env('ALGORITHM'))
        return int(payload.get("sub"))
    except (ExpiredSignatureError, JWTError) as e:
        if isinstance(e, ExpiredSignatureError):
            return JSONResponse(
                status_code=401, content={"detail": "The access token has expired"}
            )
        if isinstance(e, JWTError):
            return JSONResponse(
                status_code=401, content={"detail": "Invalid access token format"}
            )
