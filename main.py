import uvicorn
from fastapi import FastAPI
from app.routes import user_route, notes_route, auth_route
from settings import engine
from settings import Base
from app.models import User
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession



app = FastAPI(description="",
              version="0.1")

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")

app.include_router(user_route, prefix="/account", tags=["users"])
app.include_router(notes_route, prefix="/notes", tags=["notes"])
app.include_router(auth_route, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)