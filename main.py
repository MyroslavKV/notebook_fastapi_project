import uvicorn
from fastapi import FastAPI
from app.routes import user_route
from settings import engine
from app.models import User
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession



app = FastAPI(description="",
              version="0.1")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")

app.include_router(user_route, prefix="/account", tags=["users"])


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)