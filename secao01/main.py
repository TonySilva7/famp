from fastapi import FastAPI

app = FastAPI()


cursos = {
    1: {"nome": "Python", "aulas": 112, "horas": 58},
    2: {"nome": "Java", "aulas": 112, "horas": 58},
    3: {"nome": "C#", "aulas": 112, "horas": 58},
}


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True, debug=True)
