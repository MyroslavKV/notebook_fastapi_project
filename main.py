import uvicorn
from fastapi import FastAPI
from app.routes import user_route, notes_route, auth_route
from settings import engine
from settings import Base
from app.schemas import UserType
from app.models import User
from settings import async_session
from werkzeug.security import generate_password_hash
from fastapi.responses import RedirectResponse



app = FastAPI(description="", version="0.1")


async def init_bd():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_data():
    async with async_session() as sess:
        u1 = User(
            username="admin",
            email="admin@ex.com",
            password_hash=generate_password_hash("admin"),
            role=UserType.ADMIN,
            bio="Master admin",
        )
        u2 = User(
            username="user",
            email="user@ex.com",
            password_hash=generate_password_hash("user"),
            role=UserType.USER,
            bio="just user",
        )

        sess.add_all([u1, u2])
        await sess.commit()


@app.on_event("startup")
async def startup():
    await init_bd()
    print("database created")
    await insert_data()
    print("data added")
    await engine.dispose()



@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")

app.include_router(user_route, prefix="/account", tags=["users"])
app.include_router(notes_route, prefix="/notes", tags=["notes"])
app.include_router(auth_route, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)