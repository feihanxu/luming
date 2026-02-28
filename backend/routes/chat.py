from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db, ChatMessage, Person, Record, Todo
from schemas import ChatRequest, ChatResponse
from services.ai_service import AIService
import os
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=dict)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    message = ChatMessage(
        role="user",
        content=request.message,
        message_type=request.message_type
    )
    db.add(message)
    db.commit()
    
    ai_service = AIService()
    result = await ai_service.process_message(request.message, db)
    
    response_message = ChatMessage(
        role="assistant",
        content=result["response"]
    )
    db.add(response_message)
    db.commit()
    
    return result

@router.post("/confirm", response_model=dict)
async def confirm_record(draft: dict, db: Session = Depends(get_db)):
    ai_service = AIService()
    result = await ai_service.confirm_save(draft, db)
    return result

@router.post("/upload", response_model=dict)
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_DIR, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    message = ChatMessage(
        role="user",
        content=description or "",
        message_type="file",
        file_path=file_path
    )
    db.add(message)
    db.commit()
    
    ai_service = AIService()
    
    if file.content_type and file.content_type.startswith("image/"):
        result = await ai_service.process_image(file_path, description, db)
    elif file.content_type and file.content_type.startswith("audio/"):
        result = await ai_service.process_audio(file_path, description, db)
    else:
        result = {"response": "不支持的文件类型", "action": "ask", "draft": None}
    
    response_message = ChatMessage(
        role="assistant",
        content=result["response"]
    )
    db.add(response_message)
    db.commit()
    
    return result
