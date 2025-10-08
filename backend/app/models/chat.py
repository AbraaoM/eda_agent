from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.services.db import Base

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    csv_file = relationship("CSVFile", back_populates="chat", uselist=False)

class CSVFile(Base):
    __tablename__ = "csv_files"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    filename = Column(String)
    filepath = Column(String)
    chat = relationship("Chat", back_populates="csv_file")