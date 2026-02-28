from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import get_db, Record, Person
from schemas import RecordCreate, RecordResponse

router = APIRouter()

@router.get("/", response_model=List[RecordResponse])
def get_records(
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Record).order_by(Record.timestamp.desc())
    
    if start:
        query = query.filter(Record.timestamp >= datetime.fromisoformat(start))
    if end:
        query = query.filter(Record.timestamp <= datetime.fromisoformat(end))
    
    return query.all()

@router.get("/{record_id}", response_model=RecordResponse)
def get_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.post("/", response_model=RecordResponse)
def create_record(record: RecordCreate, db: Session = Depends(get_db)):
    db_record = Record(**record.dict())
    db.add(db_record)
    
    if record.person_id:
        person = db.query(Person).filter(Person.id == record.person_id).first()
        if person:
            person.last_contact = datetime.utcnow()
            person.meeting_count = (person.meeting_count or 0) + 1
    
    db.commit()
    db.refresh(db_record)
    return db_record

@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(record)
    db.commit()
    return {"message": "Record deleted"}
