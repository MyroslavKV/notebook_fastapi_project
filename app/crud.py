from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.schemas import UserCreate

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    password_hash = generate_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=password_hash
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

