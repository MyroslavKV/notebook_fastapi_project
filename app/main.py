import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(description="",
              version="0.1")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)