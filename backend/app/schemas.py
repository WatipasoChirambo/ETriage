from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# -----------------------------
# MEDICAL SCHEME
# -----------------------------
class MedicalSchemeBase(BaseModel):
    name: str
    scheme_code: Optional[str] = None
    coverage_details: Optional[str] = None

class PatientSymptomSubmission(BaseModel):
    phone_number: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    hospital_id: int
    has_scheme: bool
    medical_scheme_id: Optional[int] = None
    member_number: Optional[str] = None
    symptoms: List[int]
    severity: List[int]

class SymptomSubmission(BaseModel):
    phone_number: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    hospital_id: int
    has_scheme: bool = False
    medical_scheme_id: Optional[int] = None
    member_number: Optional[str] = None
    symptoms: List[int]
    severity: List[int]

    class Config:
        from_attributes = True

class MedicalSchemeOut(MedicalSchemeBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

# -----------------------------
# HOSPITAL
# -----------------------------
class HospitalBase(BaseModel):
    name: str
    location: Optional[str] = None

class HospitalOut(HospitalBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

# -----------------------------
# SYMPTOM
# -----------------------------
class SymptomBase(BaseModel):
    name: str
    description: Optional[str] = None

class SymptomOut(SymptomBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

# -----------------------------
# PATIENT
# -----------------------------
class PatientBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    has_scheme: bool = False
    medical_scheme_id: Optional[int] = None
    member_number: Optional[str] = None
    hospital_id: Optional[int] = None

class PatientOut(PatientBase):
    id: int
    created_at: datetime
    scheme: Optional[MedicalSchemeOut] = None
    hospital: Optional[HospitalOut] = None

    model_config = {"from_attributes": True}

# -----------------------------
# PATIENT-SYMPTOM
# -----------------------------
class PatientSymptomBase(BaseModel):
    patient_id: int
    symptom_id: int
    severity: int = 1

class PatientSymptomOut(PatientSymptomBase):
    id: int
    noted_at: datetime
    symptom: Optional[SymptomOut] = None

    model_config = {"from_attributes": True}

# -----------------------------
# TRIAGE CASE
# -----------------------------
class TriageCaseBase(BaseModel):
    patient_id: int
    triage_level: str
    recommended_action: str

class TriageCaseOut(TriageCaseBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

# -----------------------------
# ALERT
# -----------------------------
class AlertBase(BaseModel):
    patient_id: int
    triage_case_id: int
    alert_type: str
    message: str
    status: Optional[str] = "unread"

class AlertOut(AlertBase):
    id: int
    sent_at: datetime
    patient: Optional[PatientOut] = None
    triage_case: Optional[TriageCaseOut] = None

    model_config = {"from_attributes": True}

# -----------------------------
# HOSPITAL ALLOCATION
# -----------------------------
class HospitalAllocationBase(BaseModel):
    patient_id: int
    hospital_name: Optional[str] = None
    ward: Optional[str] = None
    doctor_assigned: Optional[str] = None
    status: Optional[str] = "pending"

class HospitalAllocationOut(HospitalAllocationBase):
    id: int
    allocated_at: datetime

    model_config = {"from_attributes": True}

# -----------------------------
# ADMIN
# -----------------------------
class AdminBase(BaseModel):
    name: str
    email: str
    role: str

class AdminOut(AdminBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

# -----------------------------
# SUBMIT SYMPTOMS RESPONSE (needed by FastAPI)
# -----------------------------
class SubmitSymptomsResponse(BaseModel):
    patient: PatientOut
    triage_case: TriageCaseOut

class SubmitSymptomsRequest(BaseModel):
    phone_number: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    hospital_id: int
    has_scheme: bool
    medical_scheme_id: Optional[int] = None
    member_number: Optional[str] = None
    symptoms: List[int]  # List of symptom IDs
    severity: List[int]  # List of severities corresponding to symptoms

    # Optional validation: ensure symptoms and severity lists are same length
    def validate_lengths(self):
        if len(self.symptoms) != len(self.severity):
            raise ValueError("Symptoms and severity lists must have the same length")
