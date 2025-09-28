from sqlalchemy.orm import Session
from . import models

def get_patient_by_phone(db: Session, phone: str):
    return db.query(models.Patient).filter(models.Patient.phone_number == phone).first()

def create_patient(db: Session, patient_data: dict):
    patient = models.Patient(**patient_data)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def create_patient_symptom(db: Session, patient_id: int, symptom_id: int, severity: int):
    ps = models.PatientSymptom(patient_id=patient_id, symptom_id=symptom_id, severity=severity)
    db.add(ps)
    db.commit()
    db.refresh(ps)
    return ps

def create_triage_case(db: Session, patient_id: int, level: str, action: str):
    triage = models.TriageCase(patient_id=patient_id, triage_level=level, recommended_action=action)
    db.add(triage)
    db.commit()
    db.refresh(triage)
    return triage

def create_alert(db: Session, patient_id: int, triage_case_id: int, alert_type: str, message: str):
    alert = models.Alert(patient_id=patient_id, triage_case_id=triage_case_id,
                         alert_type=alert_type, message=message)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert
