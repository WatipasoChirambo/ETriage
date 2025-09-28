from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, crud
from app.database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Triage MVP")

@router.get("/symptoms/")
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
    # 1. Get or create patient
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

    # 2. Save symptoms
    patient_symptoms = []
    for s_id, sev in zip(symptoms, severity):
        ps = crud.create_patient_symptom(db, patient.id, s_id, sev)
        patient_symptoms.append({"symptom_id": ps.symptom_id, "severity": ps.severity})

    # 3. Simple triage logic
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
