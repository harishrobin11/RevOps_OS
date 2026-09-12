from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from core.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False, index=True)
    contact_name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    industry = Column(String(100), nullable=True, index=True)
    location = Column(String(100), nullable=True, index=True)
    employee_count = Column(Integer, default=0)
    website = Column(String(255), nullable=True)
    lead_source = Column(String(100), nullable=True, index=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_contacted = Column(DateTime(timezone=True), nullable=True)
    next_follow_up = Column(DateTime(timezone=True), nullable=True, index=True)
    
    icp_score = Column(Float, default=0.0)
    priority = Column(String(50), default="Priority C", index=True)
    pipeline_stage = Column(String(100), default="Identified", index=True)
    deal_value = Column(Float, default=0.0)
    probability = Column(Float, default=0.05)
    deal_health = Column(String(50), default="Healthy")

    # Relationships
    qualifications = relationship("Qualification", back_populates="lead", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="lead", cascade="all, delete-orphan")
    outreaches = relationship("Outreach", back_populates="lead", cascade="all, delete-orphan")
    pipelines = relationship("Pipeline", back_populates="lead", cascade="all, delete-orphan")
    lead_notes = relationship("Note", back_populates="lead", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Lead id={self.id} company='{self.company_name}' stage='{self.pipeline_stage}'>"


class Qualification(Base):
    __tablename__ = "qualifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    budget_confirmed = Column(Boolean, default=False)
    authority_confirmed = Column(Boolean, default=False)
    need_confirmed = Column(Boolean, default=False)
    timeline_confirmed = Column(Boolean, default=False)
    bant_score = Column(Float, default=0.0)
    qualification_notes = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    lead = relationship("Lead", back_populates="qualifications")

    def __repr__(self):
        return f"<Qualification lead_id={self.lead_id} bant_score={self.bant_score}>"


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_type = Column(String(100), nullable=False)
    outcome = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    lead = relationship("Lead", back_populates="activities")

    def __repr__(self):
        return f"<Activity lead_id={self.lead_id} type='{self.activity_type}'>"


class Outreach(Base):
    __tablename__ = "outreaches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    channel = Column(String(100), nullable=False)
    cadence_step = Column(String(50), nullable=True)
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    status = Column(String(50), default="Pending")
    sent_at = Column(DateTime(timezone=True), nullable=True)
    response = Column(Text, nullable=True)

    lead = relationship("Lead", back_populates="outreaches")

    def __repr__(self):
        return f"<Outreach lead_id={self.lead_id} channel='{self.channel}' status='{self.status}'>"


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    stage = Column(String(100), nullable=False)
    deal_value = Column(Float, default=0.0)
    probability = Column(Float, default=0.0)
    next_action = Column(String(255), nullable=True)
    next_follow_up = Column(DateTime(timezone=True), nullable=True)
    entered_stage_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    lead = relationship("Lead", back_populates="pipelines")

    def __repr__(self):
        return f"<Pipeline lead_id={self.lead_id} stage='{self.stage}'>"


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    author = Column(String(100), default="BDA Harish")

    lead = relationship("Lead", back_populates="lead_notes")

    def __repr__(self):
        return f"<Note lead_id={self.lead_id}>"
