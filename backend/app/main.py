from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import Base, engine, get_db
from app import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="IoT Dashboard - ESP32 Sensor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "IoT backend running. POST /readings/ to send, GET /readings/ to query."}


@app.post("/readings/", response_model=schemas.ReadingOut, status_code=201)
def create_reading(reading: schemas.ReadingCreate, db: Session = Depends(get_db)):
    db_reading = models.Reading(**reading.model_dump())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading


@app.get("/readings/", response_model=List[schemas.ReadingOut])
def list_readings(limit: int = 50, db: Session = Depends(get_db)):
    return (
        db.query(models.Reading)
        .order_by(models.Reading.id.desc())
        .limit(limit)
        .all()
    )
