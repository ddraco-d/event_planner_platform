from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import router as api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Разрешенные источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешенные методы
    allow_headers=["*"],  # Разрешенные заголовки
)

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
