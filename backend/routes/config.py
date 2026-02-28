from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.ai_service import AIService
from pydantic import BaseModel

router = APIRouter()

class ConfigRequest(BaseModel):
    api_key: str
    api_url: str
    model: str

class ConfigResponse(BaseModel):
    api_key: str
    api_url: str
    model: str

@router.get("/", response_model=ConfigResponse)
def get_config(db: Session = Depends(get_db)):
    ai_service = AIService()
    config = ai_service.get_config(db)
    return ConfigResponse(
        api_key=config["api_key"][:8] + "..." if config["api_key"] else "",
        api_url=config["api_url"],
        model=config["model"]
    )

@router.post("/", response_model=ConfigResponse)
def set_config(config: ConfigRequest, db: Session = Depends(get_db)):
    ai_service = AIService()
    ai_service.set_config(config.api_key, config.api_url, config.model)
    return ConfigResponse(
        api_key=config.api_key[:8] + "...",
        api_url=config.api_url,
        model=config.model
    )
