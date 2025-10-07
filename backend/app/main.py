from fastapi import FastAPI
from app.controllers import upload_controller, prompt_controller

app = FastAPI()

app.include_router(upload_controller.router)
app.include_router(prompt_controller.router)

@app.get("/")
def read_root():
    return {"message": "EDA Agent API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)