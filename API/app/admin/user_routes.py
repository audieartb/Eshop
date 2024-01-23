from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timedelta
from app.models import AdminUserBase, AdminUser
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from app.db import getSession
from .utils import authenticate_user, create_access_token, get_current_user, create_user_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/token")

router = APIRouter()


@router.get("/user/", tags=['Admin Account'])
async def read_user(current_user: Annotated[AdminUserBase, Depends(get_current_user)],):
    return current_user


@router.post("/user", tags=['Admin Account'])
async def create_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(getSession)):

    created  = await create_user_db(username=form_data.username, password=form_data.password, session=session)
    return created
   

@router.post("/token", tags=['Admin Account'])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(getSession)):
    user = await authenticate_user(username=form_data.username,
                                   password=form_data.password,
                                   session=session)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
