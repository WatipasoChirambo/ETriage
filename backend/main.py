from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db, engine, Base, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Triage MVP")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed default symptoms
def seed_symptoms():
    db: Session = SessionLocal()
    default_symptoms = [
        {"name": "Fever", "description": "High body temperature"},
        {"name": "Cough", "description": "Persistent coughing"},
        {"name": "Headache", "description": "Pain in the head region"},
        {"name": "Shortness of breath", "description": "Difficulty breathing"},
        {"name": "Chest pain", "description": "Discomfort or tightness in the chest"},
    ]
    for s in default_symptoms:
        exists = db.query(models.Symptom).filter_by(name=s["name"]).first()
        if not exists:
            crud.create_symptom(db, s["name"], s["description"])
    db.close()

seed_symptoms()

# Get all symptoms
@app.get("/symptoms/")
def get_symptoms(db: Session = Depends(get_db)):
    return db.query(models.Symptom).all()


# Submit symptoms endpoint
@app.post("/submit_symptoms/")
def submit_symptoms(submission: schemas.SymptomSubmission, db: Session = Depends(get_db)):
    data = submission.dict()

    # 1. Get or create patient
    patient = crud.get_patient_by_phone(db, data["phone_number"])
    if not patient:
        patient_data = {
            "phone_number": data["phone_number"],
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "has_scheme": data.get("has_scheme", False),
            "medical_scheme_id": data.get("medical_scheme_id"),
            "member_number": data.get("member_number")
        }
        patient = crud.create_patient(db, patient_data)

    # 2. Save symptoms
    patient_symptoms = []
    for s_id, sev in zip(data["symptoms"], data["severity"]):
        ps = crud.create_patient_symptom(db, patient.id, s_id, sev)
        patient_symptoms.append({"symptom_id": ps.symptom_id, "severity": ps.severity})

    # 3. Simple triage logic
    max_sev = max(data["severity"]) if data["severity"] else 1
    if max_sev == 3:
        triage_level = "high"
        action = "Visit hospital immediately"
    elif max_sev == 2:
        triage_level = "medium"
        action = "Monitor symptoms; visit hospital if worsens"
    else:
        triage_level = "low"
        action = "Home care recommended"

    triage_case = crud.create_triage_case(db, patient.id, triage_level, action)

    # 4. Create alert if critical
    if triage_level == "high":
        crud.create_alert(
            db, patient.id, triage_case.id, "critical", f"Patient {patient.id} requires attention!"
        )

    # 5. Return full patient info for frontend
    return {
        "patient": {
            "id": patient.id,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "phone_number": patient.phone_number,
            "has_scheme": patient.has_scheme,
            "medical_scheme_id": patient.medical_scheme_id,
            "member_number": patient.member_number,
            "symptoms": patient_symptoms
        },
        "triage_case": {
            "id": triage_case.id,
            "triage_level": triage_level,
            "recommended_action": action
        }
    }
