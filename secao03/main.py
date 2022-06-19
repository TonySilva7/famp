from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router

app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    version="0.0.1",
    redoc_config={
        "spec_url": f"{settings.API_V1_STR}/openapi.json",
        "expand_all": True,
        "hide_hostname": True,
        "theme": "dark",
        "path_in_middle": True,
        "default_expand": True,
    },
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        debug=True,
        log_level="info",
        access_log=False,
    )
