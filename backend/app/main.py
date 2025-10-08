from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import upload_controller, prompt_controller
from app.services.db import Base, engine

app = FastAPI()

# Configuração do CORS para aceitar requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_controller.router)
app.include_router(prompt_controller.router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "EDA Agent API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)