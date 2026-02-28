from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PersonBase(BaseModel):
    name: str
    title: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    avatar: Optional[str] = None
    tags: Optional[List[str]] = []
    preferences: Optional[dict] = {}

class PersonCreate(PersonBase):
    pass

class PersonUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    avatar: Optional[str] = None
    tags: Optional[List[str]] = None
    preferences: Optional[dict] = None

class PersonResponse(PersonBase):
    id: int
    last_contact: Optional[datetime] = None
    meeting_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class RecordBase(BaseModel):
    person_id: Optional[int] = None
    person_name: Optional[str] = None
    person_title: Optional[str] = None
    person_company: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[str] = None
    topic: Optional[str] = None
    todo: Optional[str] = None
    note: Optional[str] = None
    raw_input: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordResponse(RecordBase):
    id: int
    timestamp: datetime
    created_at: datetime
    
    class Config:
        orm_mode = True

class TodoBase(BaseModel):
    content: str
    person_id: Optional[int] = None
    record_id: Optional[int] = None
    due_date: Optional[datetime] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    completed: Optional[bool] = None
    content: Optional[str] = None

class TodoResponse(TodoBase):
    id: int
    completed: bool
    record_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    message: str
    message_type: str = "text"

class ChatResponse(BaseModel):
    response: str
    record: Optional[dict] = None
    avatar_update: Optional[dict] = None
