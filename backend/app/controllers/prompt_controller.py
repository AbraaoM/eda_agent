from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.agent_service import agent
from app.services.db import SessionLocal
from app.models.chat import Chat, CSVFile

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PromptRequest(BaseModel):
    prompt: str
    chat_id: int

@router.post("/prompt/")
async def execute_prompt(request: PromptRequest, db: Session = Depends(get_db)):
    # Buscar o chat e seu CSV associado
    chat = db.query(Chat).filter(Chat.id == request.chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail=f"Chat {request.chat_id} não encontrado.")
    
    if not chat.csv_file:
        raise HTTPException(status_code=404, detail=f"Nenhum CSV associado ao chat {request.chat_id}.")
    
    # Carregar o CSV no singleton antes de processar o prompt
    result = agent.handle_prompt(request.prompt, chat.csv_file.filepath)
    if result is None:
        raise HTTPException(status_code=500, detail="Erro ao processar o prompt.")
    return result