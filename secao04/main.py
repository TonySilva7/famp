from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router


app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    openapi_url=settings.API_V1_STR,
    docs_url=settings.API_DOCS_STR,
    redoc_url=settings.API_REDOC_STR,
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True, debug=True)
    # uvicorn.run(app, host="localhost", port=8000, reload=True) # reload=True for development only
    # uvicorn.run(app, host="localhost", port=8000, reload=True, debug=True)  # reload=True for development only
    # uvicorn.run(app, host="localhost", port=8000, reload=True, debug=True, log_level="info")  # reload=True for development only
    # uvicorn.run(app, host="localhost", port=8000, reload=True, debug=True, log_level="info", workers=1)  # reload=True for development only
    # uvicorn.run(app, host="localhost", port=8000, reload=True, debug=True, log_level="info", workers=1, access_log=True)  # reload=True for development only
    # uvicorn.run(app, host="localhost", port=8000, reload=True, debug=True, log_level="info", workers=1, access_log=True, error_log=True)  # reload=True for development only
    # uvicorn.run(app, host="localhost", port=8000, reload=True, debug=True, log_level="info", workers=1, access_log=True, error_log=True, proxy_headers=True)  # reload=True for development only
    # uvicorn.run(app, host="localhost", port=8000, reload=True, debug=True, log_level="info", workers=1, access_log=True, error_log=True, proxy_headers=True, proxy_allow_all=True)  # reload=True for development only
    # uvicorn.run(app, host="localhost", port=8000, reload=True, debug=True, log_level="info", workers=1, access_log=True, error_log=True, proxy_headers=True, proxy_allow_all=True, lifespan="on_startup")  # reload
