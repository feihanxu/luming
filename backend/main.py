from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables
from routes import persons, records, todos, chat, config

create_tables()

app = FastAPI(
    title="鹿鸣 API",
    description="个人人脉管理助手后端",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(persons.router, prefix="/api/persons", tags=["persons"])
app.include_router(records.router, prefix="/api/records", tags=["records"])
app.include_router(todos.router, prefix="/api/todos", tags=["todos"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(config.router, prefix="/api/config", tags=["config"])

@app.get("/")
async def root():
    return {"message": "鹿鸣 API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
