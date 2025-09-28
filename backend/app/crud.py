from sqlalchemy.orm import Session
from . import models
from app import schemas
from typing import Optional, Dict


# -----------------------------
# SYMPTOM CRUD
# -----------------------------
def create_symptom(db: Session, name: str, description: Optional[str] = "") -> models.Symptom:
    symptom = models.Symptom(name=name, description=description)
    db.add(symptom)
    db.commit()
    db.refresh(symptom)
    return symptom


# -----------------------------
# PATIENT CRUD
# -----------------------------
def get_patient_by_phone(db: Session, phone: str, hospital_id: Optional[int] = None) -> Optional[models.Patient]:
    query = db.query(models.Patient).filter(models.Patient.phone_number == phone)
    if hospital_id is not None:
        query = query.filter(models.Patient.hospital_id == hospital_id)
    return query.first()


def create_patient(db: Session, patient_data: Dict) -> models.Patient:
    """
    patient_data is a dictionary matching Patient fields.
    Ensures hospital_id and medical_scheme_id are integers if provided.
    """
    if "hospital_id" in patient_data and patient_data["hospital_id"] is not None:
        patient_data["hospital_id"] = int(patient_data["hospital_id"])
    if "medical_scheme_id" in patient_data and patient_data["medical_scheme_id"] is not None:
        patient_data["medical_scheme_id"] = int(patient_data["medical_scheme_id"])
    
    patient = models.Patient(**patient_data)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


# -----------------------------
# PATIENT-SYMPTOMS
# -----------------------------
def create_patient_symptom(db: Session, patient_id: int, symptom_id: int, severity: int = 1) -> models.PatientSymptom:
    ps = models.PatientSymptom(patient_id=patient_id, symptom_id=symptom_id, severity=severity)
    db.add(ps)
    db.commit()
    db.refresh(ps)
    return ps


# -----------------------------
# TRIAGE CASES
# -----------------------------
def create_triage_case(db: Session, patient_id: int, level: str, action: str) -> models.TriageCase:
    triage = models.TriageCase(patient_id=patient_id, triage_level=level, recommended_action=action)
    db.add(triage)
    db.commit()
    db.refresh(triage)
    return triage


# -----------------------------
# ALERTS
# -----------------------------
def create_alert(db: Session, patient_id: int, triage_case_id: int, alert_type: str, message: str) -> models.Alert:
    alert = models.Alert(
        patient_id=patient_id,
        triage_case_id=triage_case_id,
        alert_type=alert_type,
        message=message
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert
