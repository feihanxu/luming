from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db, Person
from schemas import PersonCreate, PersonUpdate, PersonResponse

router = APIRouter()

@router.get("/", response_model=List[PersonResponse])
def get_persons(db: Session = Depends(get_db)):
    return db.query(Person).all()

@router.get("/{person_id}", response_model=PersonResponse)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.post("/", response_model=PersonResponse)
def create_person(person: PersonCreate, db: Session = Depends(get_db)):
    db_person = Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@router.put("/{person_id}", response_model=PersonResponse)
def update_person(person_id: int, person: PersonUpdate, db: Session = Depends(get_db)):
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    update_data = person.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_person, key, value)
    
    db.commit()
    db.refresh(db_person)
    return db_person

@router.delete("/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    db.delete(db_person)
    db.commit()
    return {"message": "Person deleted"}
