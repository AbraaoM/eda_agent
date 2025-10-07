from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.agent_service import agent

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/prompt/")
async def execute_prompt(request: PromptRequest):
    result = agent.handle_prompt(request.prompt)
    if result is None:
        raise HTTPException(status_code=500, detail="Erro ao processar o prompt.")
    return {"result": result}