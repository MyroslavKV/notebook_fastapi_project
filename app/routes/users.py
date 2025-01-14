from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_user, authenticate_user, get_user_by_email
from app.schemas import UserCreate, UserLogin, UserOut
from app.security import create_access_token, get_current_user
from app.models import User
from settings import get_db

route = APIRouter(
    prefix="/users",
    tags=["users"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Users #
@route.post("/users/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    new_user = await create_user(db, user)
    return new_user

@route.post("/users/login", status_code=status.HTTP_200_OK)
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    auth_user = await authenticate_user(db, user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")
    token = create_access_token({"sub": auth_user.email})
    return {"access_token": token, "token_type": "bearer"}

@route.get("/users/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user