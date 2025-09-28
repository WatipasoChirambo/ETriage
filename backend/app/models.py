from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# -----------------------------
# MEDICAL SCHEMES
# -----------------------------
class MedicalScheme(Base):
    __tablename__ = "medical_schemes"
    __table_args__ = {"extend_existing": True}  # needed if the table already exists

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    scheme_code = Column(String, nullable=True)
    coverage_details = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    patients = relationship("Patient", back_populates="scheme")


# -----------------------------
# HOSPITALS
# -----------------------------
class Hospital(Base):
    __tablename__ = "hospitals"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    patients = relationship("Patient", back_populates="hospital")
    allocations = relationship("HospitalAllocation", back_populates="hospital")


# -----------------------------
# PATIENTS
# -----------------------------
class Patient(Base):
    __tablename__ = "patients"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    has_scheme = Column(Boolean, default=False)
    medical_scheme_id = Column(Integer, ForeignKey("medical_schemes.id"), nullable=True)
    member_number = Column(String, nullable=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    scheme = relationship("MedicalScheme", back_populates="patients")
    hospital = relationship("Hospital", back_populates="patients")
    symptoms = relationship("PatientSymptom", back_populates="patient")
    triage_cases = relationship("TriageCase", back_populates="patient")
    alerts = relationship("Alert", back_populates="patient")
    allocations = relationship("HospitalAllocation", back_populates="patient")


# -----------------------------
# SYMPTOMS
# -----------------------------
class Symptom(Base):
    __tablename__ = "symptoms"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    patient_symptoms = relationship("PatientSymptom", back_populates="symptom")


# -----------------------------
# PATIENT-SYMPTOM RELATION
# -----------------------------
class PatientSymptom(Base):
    __tablename__ = "patient_symptoms"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    symptom_id = Column(Integer, ForeignKey("symptoms.id"), nullable=False)
    severity = Column(Integer, default=1, nullable=False)
    noted_at = Column(TIMESTAMP, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="symptoms")
    symptom = relationship("Symptom", back_populates="patient_symptoms")


# -----------------------------
# TRIAGE CASES
# -----------------------------
class TriageCase(Base):
    __tablename__ = "triage_cases"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    triage_level = Column(String, nullable=False)
    recommended_action = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="triage_cases")
    alerts = relationship("Alert", back_populates="triage_case")


# -----------------------------
# ALERTS
# -----------------------------
class Alert(Base):
    __tablename__ = "alerts"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    triage_case_id = Column(Integer, ForeignKey("triage_cases.id"), nullable=False)
    alert_type = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(String, default="unread", nullable=False)

    patient = relationship("Patient", back_populates="alerts")
    triage_case = relationship("TriageCase", back_populates="alerts")


# -----------------------------
# HOSPITAL ALLOCATIONS
# -----------------------------
class HospitalAllocation(Base):
    __tablename__ = "hospital_allocations"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    ward = Column(String, nullable=True)
    doctor_assigned = Column(String, nullable=True)
    status = Column(String, default="pending", nullable=False)
    allocated_at = Column(TIMESTAMP, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="allocations")
    hospital = relationship("Hospital", back_populates="allocations")


# -----------------------------
# ADMINS
# -----------------------------
class Admin(Base):
    __tablename__ = "admins"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
