from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services import csv_service
from app.models.chat import Chat, CSVFile
from app.services.db import SessionLocal
import shutil
import os
from datetime import datetime

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/chats/")
async def create_chat_with_csv(
    file: UploadFile = File(...),
    name: str = None,
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    # Ler o conteúdo do arquivo uma única vez
    content = await file.read()
    
    # Processar CSV primeiro para validar
    try:
        rows = csv_service.process_csv(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

    # Criar chat no banco
    chat = Chat(name=name or f"Chat {datetime.utcnow()}")
    db.add(chat)
    db.commit()
    db.refresh(chat)

    # Salvar arquivo CSV
    csv_filename = f"{chat.id}_{file.filename}"
    csv_path = os.path.join("data", "csv", csv_filename)
    
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    # Salvar arquivo
    with open(csv_path, "wb") as buffer:
        buffer.write(content)  # Usar o conteúdo já lido

    # Criar registro do CSV
    csv_file = CSVFile(
        chat_id=chat.id,
        filename=file.filename,
        filepath=csv_path
    )
    db.add(csv_file)
    db.commit()

    return {
        "chat_id": chat.id,
        "name": chat.name,
        "filename": file.filename,
        "rows": rows
    }

@router.get("/chats/")
def list_chats(db: Session = Depends(get_db)):
    chats = db.query(Chat).all()
    return chats

@router.get("/chats/{chat_id}")
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat