from fastapi import FastAPI
from routes import curso_router

app = FastAPI(
    title="Cursos API",
    description="API para acesso aos cursos",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
)


app.include_router(curso_router.router, tags=["cursos"], prefix="/api/v1")


# Entry point of the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True, debug=True)
