from fastapi import FastAPI

from backend.config.settings import settings

from backend.api.chat import router as chat_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.include_router(
    chat_router,
    prefix=settings.API_PREFIX,
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


@app.get("/health", tags=["Health"]) # health check endpoint
async def health_check() -> dict:
    """
    Report whether the API process is running and able to answer requests.
    """

    return {
        "status": "healthy",
    }
