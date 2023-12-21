from typing import Annotated, Union
from datetime import datetime, timedelta
from app.models import AdminUserBase, AdminUser
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import SQLModel, select
from app.db import getSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/token")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str, session: AsyncSession):
    print(username)
    result = await session.exec(select(AdminUser).where(AdminUser.username == username))
    user = result.one_or_none()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_user_db(username: str, password: str,session: AsyncSession ):
    data = await session.exec(
        select(AdminUser).where(AdminUser.username == username))
    user = data.one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="Username Already Exists")

    hashed_password = get_password_hash(password=password)
    db_user = AdminUser(username=username, hashed_password=hashed_password)
    session.add(db_user)
    await session.commit()
    await session.close()
    return


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(getSession)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Invalid Authentication Credentials",
                                         headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credential_exception
    user = await session.exec(select(AdminUser).where(
        AdminUser.username == token_data.username))
    if not user:
        raise credential_exception
    return user.one()
