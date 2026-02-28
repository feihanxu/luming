from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./luming.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

class Person(Base):
    __tablename__ = "persons"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    title = Column(String(100))
    company = Column(String(200))
    industry = Column(String(100))
    avatar = Column(String(500))
    tags = Column(JSON, default=list)
    preferences = Column(JSON, default=dict)
    last_contact = Column(DateTime)
    meeting_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    records = relationship("Record", back_populates="person")
    todos = relationship("Todo", back_populates="person")

class Record(Base):
    __tablename__ = "records"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    person_name = Column(String(100))
    person_title = Column(String(100))
    person_company = Column(String(200))
    timestamp = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)
    location = Column(String(200))
    topic = Column(String(200))
    todo = Column(String(500))
    note = Column(Text)
    raw_input = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    person = relationship("Person", back_populates="records")

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    record_id = Column(Integer, ForeignKey("records.id"))
    content = Column(String(500), nullable=False)
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime)
    record_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    person = relationship("Person", back_populates="todos")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(20))
    content = Column(Text)
    message_type = Column(String(20), default="text")
    file_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
