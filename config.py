import os

# Base Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "pipeline.db")
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"

# Product Metadata
PRODUCT_NAME = "RevOps OS"
PRODUCT_FULL_NAME = "RevOps OS — B2B Lead Intelligence & Revenue Pipeline Platform"
COMPANY_NAME = "Avgova Solutions"
VERSION = "1.0.0"

# Target ICP Default Settings (Bangalore B2B Tech & Services)
TARGET_INDUSTRIES = [
    "SaaS",
    "IT Services",
    "FinTech",
    "HealthTech",
    "Logistics",
    "Professional Services",
    "Technology Services",
    "B2B Platforms"
]

TARGET_TERRITORIES = [
    "Outer Ring Road",
    "Whitefield",
    "Koramangala",
    "Electronic City",
    "HSR Layout",
    "Indiranagar",
    "Bellandur"
]

DECISION_MAKER_ROLES = [
    "COO",
    "VP Business Operations",
    "Head of Operations",
    "Head of Delivery",
    "Operations Director",
    "Founder",
    "Business Unit Head"
]

LEAD_SOURCES = [
    "Inbound Website",
    "Outbound Cold Outreach",
    "LinkedIn Prospecting",
    "Industry Conference",
    "Partner Referral",
    "Exhibition / Event"
]

# Pipeline Stages
PIPELINE_STAGES = [
    "Identified",
    "Contacted",
    "Engaged",
    "Qualified",
    "Discovery Booked",
    "Proposal",
    "Negotiation",
    "Won",
    "Lost",
    "Nurture"
]

STAGE_PROBABILITIES = {
    "Identified": 0.05,
    "Contacted": 0.10,
    "Engaged": 0.20,
    "Qualified": 0.35,
    "Discovery Booked": 0.50,
    "Proposal": 0.70,
    "Negotiation": 0.85,
    "Won": 1.00,
    "Lost": 0.00,
    "Nurture": 0.10
}

# ICP Scoring Weights (Total = 100)
ICP_WEIGHTS = {
    "industry_fit": 20,
    "company_size_fit": 15,
    "territory_fit": 15,
    "decision_maker_fit": 20,
    "pain_point_fit": 20,
    "growth_signal": 10
}

# BANT Scoring Weights (Total = 100)
BANT_WEIGHTS = {
    "budget": 25,
    "authority": 35,
    "need": 25,
    "timeline": 15
}

# Combined Priority Score Thresholds
PRIORITY_CRITICAL = 85
PRIORITY_HIGH = 70
PRIORITY_MEDIUM = 50

# UI Theme Color Palette (Executive Dark SaaS Theme)
THEME_COLORS = {
    "bg_dark": "#0B0F19",
    "card_bg": "#111827",
    "card_border": "#1F2937",
    "primary_accent": "#3B82F6",
    "primary_hover": "#2563EB",
    "text_main": "#F9FAFB",
    "text_muted": "#9CA3AF",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#06B6D4"
}
