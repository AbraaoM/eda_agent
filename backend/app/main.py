from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "EDA Agent API is running"}