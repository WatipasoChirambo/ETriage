from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, models, schemas
from app.database import get_db, engine, Base, SessionLocal

app = FastAPI(title="Hospital Triage MVP")

# ----------------------
# Enable CORS
# ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Medical Schemes
# ----------------------
@app.get("/medical_schemes/", response_model=List[schemas.MedicalSchemeOut])
def get_medical_schemes(db: Session = Depends(get_db)):
    return db.query(models.MedicalScheme).all()

# ----------------------
# Startup event
# ----------------------
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    seed_symptoms()
    seed_hospitals()
    seed_schemes()

# ----------------------
# Seed functions
# ----------------------
def seed_symptoms():
    db: Session = SessionLocal()
    try:
        default_symptoms = [
            {"name": "Fever", "description": "High body temperature"},
            {"name": "Cough", "description": "Persistent coughing"},
            {"name": "Headache", "description": "Pain in the head region"},
            {"name": "Shortness of breath", "description": "Difficulty breathing"},
            {"name": "Chest pain", "description": "Discomfort or tightness in the chest"},
        ]
        for s in default_symptoms:
            if not db.query(models.Symptom).filter_by(name=s["name"]).first():
                crud.create_symptom(db, s["name"], s["description"])
    finally:
        db.close()


def seed_hospitals():
    db: Session = SessionLocal()
    try:
        default_hospitals = [
            {"name": "Central Hospital", "location": "City Center"},
            {"name": "Community Clinic", "location": "Suburbs"},
        ]
        for h in default_hospitals:
            if not db.query(models.Hospital).filter_by(name=h["name"]).first():
                db.add(models.Hospital(name=h["name"], location=h["location"]))
        db.commit()
    finally:
        db.close()


def seed_schemes():
    db: Session = SessionLocal()
    try:
        default_schemes = [
            {"name": "HealthPlus"},
            {"name": "MediCare"},
        ]
        for s in default_schemes:
            exists = db.query(models.MedicalScheme).filter_by(name=s["name"]).first()
            if not exists:
                scheme = models.MedicalScheme(name=s["name"])
                db.add(scheme)
        db.commit() 
    finally:
        db.close()



# ----------------------
# READ endpoints
# ----------------------
@app.get("/hospitals/", response_model=List[schemas.HospitalOut])
def get_hospitals(db: Session = Depends(get_db)):
    return db.query(models.Hospital).all()


@app.get("/symptoms/", response_model=List[schemas.SymptomOut])
def get_symptoms(db: Session = Depends(get_db)):
    return db.query(models.Symptom).all()


@app.get("/medical_schemes/", response_model=List[schemas.MedicalSchemeOut])
def get_medical_schemes(db: Session = Depends(get_db)):
    return db.query(models.MedicalScheme).all()


# ----------------------
# SUBMIT SYMPTOMS
# ----------------------
@app.post("/submit_symptoms/", response_model=schemas.SubmitSymptomsResponse)
def submit_symptoms(submission: schemas.SubmitSymptomsRequest, db: Session = Depends(get_db)):

    # Optional: validate lengths
    try:
        submission.validate_lengths()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Check if patient exists
    patient = crud.get_patient_by_phone(db, submission.phone_number, submission.hospital_id)
    if not patient:
        patient_data = {
            "phone_number": submission.phone_number,
            "first_name": submission.first_name or "Unknown",
            "last_name": submission.last_name or "",
            "has_scheme": submission.has_scheme,
            "hospital_id": submission.hospital_id,
            "medical_scheme_id": submission.medical_scheme_id,
            "member_number": submission.member_number,
        }
        patient = crud.create_patient(db, patient_data)

    # Add all submitted symptoms
    for symptom_id, severity in zip(submission.symptoms, submission.severity):
        crud.create_patient_symptom(db, patient.id, symptom_id, severity)

    # Create a default triage case (replace logic as needed)
    triage_case = crud.create_triage_case(db, patient.id, "low", "Home care recommended")

    return schemas.SubmitSymptomsResponse(
        patient=schemas.PatientOut.from_orm(patient),
        triage_case=schemas.TriageCaseOut.from_orm(triage_case)
    )

