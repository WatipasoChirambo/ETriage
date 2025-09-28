from typing import Optional, List
from pydantic import BaseModel


# -----------------------------
# SYMPTOMS
# -----------------------------
class SymptomBase(BaseModel):
    name: str
    description: Optional[str] = None


class SymptomCreate(SymptomBase):
    pass


class SymptomOut(SymptomBase):
    id: int

    class Config:
        orm_mode = True


# -----------------------------
# PATIENTS
# -----------------------------
class PatientBase(BaseModel):
    phone_number: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    has_scheme: bool = False
    medical_scheme_id: Optional[int] = None
    member_number: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientOut(PatientBase):
    id: int

    class Config:
        orm_mode = True


# -----------------------------
# PATIENT-SYMPTOM RELATION
# -----------------------------
class PatientSymptomBase(BaseModel):
    symptom_id: int
    severity: int


class PatientSymptomCreate(PatientSymptomBase):
    patient_id: int


class PatientSymptomOut(PatientSymptomBase):
    id: int
    patient_id: int

    class Config:
        orm_mode = True


# -----------------------------
# TRIAGE CASES
# -----------------------------
class TriageCaseBase(BaseModel):
    triage_level: str
    action: str


class TriageCaseCreate(TriageCaseBase):
    patient_id: int


class TriageCaseOut(TriageCaseBase):
    id: int
    patient_id: int

    class Config:
        orm_mode = True


# -----------------------------
# ALERTS
# -----------------------------
class AlertBase(BaseModel):
    level: str
    message: str


class AlertCreate(AlertBase):
    patient_id: int
    case_id: int


class AlertOut(AlertBase):
    id: int
    patient_id: int
    case_id: int

    class Config:
        orm_mode = True


# -----------------------------
# COMBINED RESPONSE FOR SUBMISSION
# -----------------------------
class SubmitSymptomsResponse(BaseModel):
    patient: PatientOut
    triage_case: TriageCaseOut

    class Config:
        orm_mode = True
