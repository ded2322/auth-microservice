from fastapi import APIRouter
from starlette.responses import JSONResponse

from core.utils.auth import get_password_hash, create_access_token, decode_jwt_user_id, verification_password
from core.schemas.schema import UserSchema, JwtSchema
from core.dao.user_dao import UserDao
from core.config import logger

router = APIRouter(
    prefix="/user",
    tags=["Service User"],
)


@router.post("/register-super-user", status_code=201,summary="Register Superuser")
async def register_super_user(user_data: UserSchema):
    """
    Позволяет заригестировать супер-пользователя.
    Возвращает 201 статус код
    """
    logger.info("Register Superuser")

    if await UserDao.found_one_or_none(username=user_data.username):
        return JSONResponse(status_code=409, content={"detail": "Username already registered"})

    if len(user_data.username) > 30:
        return JSONResponse(status_code=409, content={"detail": "Username too long"})

    await UserDao.insert_data(username=user_data.username,
                              hash_password=get_password_hash(user_data.password),
                              is_superuser=True)

    return JSONResponse(status_code=201, content={"detail": "Super user created successfully"})


@router.post("/register-user",status_code=201,summary="Register user")
async def register_user(user_data: UserSchema):
    """
    Позволяет заригестировать пользователя.
    Возвращает 201 статус код
    """
    logger.info("Register user")
    if await UserDao.found_one_or_none(username=user_data.username):
        logger.error("Username already registered")
        return JSONResponse(status_code=409, content={"detail": "Username already registered"})

    if len(user_data.username) > 30:
        logger.error("Username too long")
        return JSONResponse(status_code=409, content={"detail": "Username too long"})

    await UserDao.insert_data(username=user_data.username,
                              hash_password=get_password_hash(user_data.password), )

    return JSONResponse(status_code=201, content={"detail": "User created successfully"})


@router.post("/login",status_code=200,summary="Login user")
async def login_user(input_data: UserSchema):
    """
    Позволяет войти в аккаунт.
    Возвращает jwt-токен
    """
    logger.info("Login user")
    try:
        user_data = await UserDao.found_one_or_none(username=input_data.username)
        if not user_data or not verification_password(input_data.password, user_data.hash_password):
            logger.error("Fail logging in user")
            return JSONResponse(status_code=409, content={"detail": "Invalid credentials"})

        jwt_token = create_access_token({"sub": str(user_data.id)})

        return {"token": jwt_token}

    except Exception as e:
        print(f"Error in login_user: {str(e)}")


@router.post("/decode-jwt", status_code=200,summary="Decode a JWT", tags=["JWT"])
async def decode_jwt(token: JwtSchema):
    """
    Декодирует jwt токен.
    Возвращает данные по пользователю
    """
    logger.info("Decode a JWT")
    try:
        user_id = decode_jwt_user_id(token.token)

        if (not user_id) or isinstance(user_id, JSONResponse):
            logger.error("Fail to decode jwt")
            return JSONResponse(status_code=409, content={"detail": "Invalid JWT token"})

        return await UserDao.user_info(id=user_id)
    except Exception as e:
        print(f"Error in decode_jwt: {str(e)}")

