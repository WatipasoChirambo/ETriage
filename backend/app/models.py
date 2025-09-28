from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from app import schemas
from .database import Base
from datetime import datetime

class MedicalScheme(Base):
    __tablename__ = "medical_schemes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    scheme_code = Column(String)
    coverage_details = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, unique=True)
    date_of_birth = Column(Date)
    gender = Column(String)
    has_scheme = Column(Boolean, default=False)
    medical_scheme_id = Column(Integer, ForeignKey("medical_schemes.id"), nullable=True)
    member_number = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    scheme = relationship("MedicalScheme")

class Symptom(Base):
    __tablename__ = "symptoms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class PatientSymptom(Base):
    __tablename__ = "patient_symptoms"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    symptom_id = Column(Integer, ForeignKey("symptoms.id"))
    severity = Column(Integer, default=1)
    noted_at = Column(TIMESTAMP, default=datetime.utcnow)

class TriageCase(Base):
    __tablename__ = "triage_cases"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    triage_level = Column(String)
    recommended_action = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class HospitalAllocation(Base):
    __tablename__ = "hospital_allocations"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    hospital_name = Column(String)
    ward = Column(String)
    doctor_assigned = Column(String)
    status = Column(String, default="pending")
    allocated_at = Column(TIMESTAMP, default=datetime.utcnow)

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    triage_case_id = Column(Integer, ForeignKey("triage_cases.id"))
    alert_type = Column(String)
    message = Column(Text)
    sent_at = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(String, default="unread")
