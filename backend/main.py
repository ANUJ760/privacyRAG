from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.chat import router as chat_router
from backend.api.upload import router as upload_router
from backend.config.settings import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.include_router(
    chat_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    upload_router,
    prefix=settings.API_PREFIX,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGIN_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root() -> dict:
    """
    Return basic application metadata for the root API endpoint.
    """

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """
    Report whether the API process is running and able to answer requests.
    """

    return {
        "status": "healthy",
    }
