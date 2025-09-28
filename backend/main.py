from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models, crud, schemas
from app.database import engine, Base, get_db, SessionLocal

# 1. Create database tables
Base.metadata.create_all(bind=engine)

# 2. Initialize FastAPI app
app = FastAPI(title="Hospital Triage MVP")

# 3. Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins, change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Seed default symptoms
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

# 5. Routes
@app.get("/symptoms/")
def get_symptoms(db: Session = Depends(get_db)):
    return db.query(models.Symptom).all()

@app.get("/triage_cases/")
def get_triage_cases(db: Session = Depends(get_db)):
    cases = db.query(models.TriageCase).all()
    result = []
    for case in cases:
        patient = db.query(models.Patient).filter(models.Patient.id == case.patient_id).first()
        symptoms = db.query(models.PatientSymptom).filter(models.PatientSymptom.patient_id == patient.id).all()
        result.append({
            "id": case.id,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "phone_number": patient.phone_number,
            "symptoms": [s.symptom_id for s in symptoms],
            "severity": [s.severity for s in symptoms],
            "triage_level": case.triage_level,
            "recommended_action": case.action
        })
    return result

@app.post("/submit_symptoms/")
def submit_symptoms(
    phone_number: str,
    first_name: str = None,
    last_name: str = None,
    has_scheme: bool = False,
    medical_scheme_id: int = None,
    member_number: str = None,
    symptoms: list[int] = [],
    severity: list[int] = [],
    db: Session = Depends(get_db)
):
    # Get or create patient
    patient = crud.get_patient_by_phone(db, phone_number)
    if not patient:
        patient_data = {
            "phone_number": phone_number,
            "first_name": first_name,
            "last_name": last_name,
            "has_scheme": has_scheme,
            "medical_scheme_id": medical_scheme_id,
            "member_number": member_number
        }
        patient = crud.create_patient(db, patient_data)

    # Save symptoms
    patient_symptoms = []
    for s_id, sev in zip(symptoms, severity):
        ps = crud.create_patient_symptom(db, patient.id, s_id, sev)
        patient_symptoms.append({"symptom_id": ps.symptom_id, "severity": ps.severity})

    # Simple triage logic
    max_sev = max(severity) if severity else 1
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

    # Create alert if critical
    if triage_level == "high":
        crud.create_alert(
            db, patient.id, triage_case.id, "critical", f"Patient {patient.id} requires attention!"
        )

    # Return patient info for frontend
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
