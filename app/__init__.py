import asyncio

from werkzeug.security import generate_password_hash

from settings import Base, async_session, engine
from app.schemas import UserType
from app.models import User


async def create_bd():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_data():
    async with async_session() as sess:
        u1 = User(username="admin",
                  email="admin@ex.com",
                  password_hash=generate_password_hash("admin"),
                  role=UserType.ADMIN,
                  bio="Master admin",
                  )
        u2 = User(username="user",
                  email="user@ex.com",
                  password_hash=generate_password_hash("user"),
                  role=UserType.USER,
                  bio="just user",
                  )
        await sess.commit()


async def main():
    await create_bd()
    print("database created")
    await insert_data()
    print("data added")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())