import os
import sys
from datetime import datetime, timedelta, timezone

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from core.database import init_db, get_db
from core.models import Lead, Qualification, Activity, Outreach, Pipeline, Note


def get_fictional_leads_data():
    """
    Generate 28 realistic fictional Bangalore B2B account records.
    """
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    
    return [
        # Priority A / High Value Opportunities (5)
        {
            "company_name": "VertexCloud Technologies",
            "contact_name": "Rajesh Varma",
            "title": "Chief Operating Officer",
            "email": "rajesh.varma@vertexcloud-demo.in",
            "phone": "+91 98450 11223",
            "industry": "SaaS",
            "location": "Outer Ring Road",
            "employee_count": 180,
            "website": "https://vertexcloud-demo.in",
            "lead_source": "Outbound Cold Outreach",
            "notes": "Fast-growing B2B SaaS scaling from 100 to 200 engineers. Struggling with fragmented CRM tracking and slow sales follow-up cadences.",
            "created_at": now - timedelta(days=25),
            "updated_at": now - timedelta(days=1),
            "last_contacted": now - timedelta(days=2),
            "next_follow_up": now - timedelta(days=1),  # Overdue
            "icp_score": 92.0,
            "priority": "Priority A",
            "pipeline_stage": "Negotiation",
            "deal_value": 4500000.0,
            "probability": 0.85,
            "deal_health": "Healthy",
            "bant": {"budget": True, "authority": True, "need": True, "timeline": True, "score": 95.0, "notes": "Budget approved ₹45L per annum. COO is decision maker."},
            "activities": [
                {"type": "Call", "outcome": "Connected with COO", "notes": "Discussed process bottlenecks in current outreach. Scheduled demo."},
                {"type": "Meeting", "outcome": "Discovery Completed", "notes": "Presented RevOps pipeline management solution. High interest."},
                {"type": "Stage Change", "outcome": "Moved to Negotiation", "notes": "Submitted commercial proposal for 50 licenses."}
            ]
        },
        {
            "company_name": "FinEdge Logistics Systems",
            "contact_name": "Ananya Rao",
            "title": "VP Business Operations",
            "email": "ananya.rao@finedgelogistics-demo.com",
            "phone": "+91 99001 22334",
            "industry": "FinTech",
            "location": "Koramangala",
            "employee_count": 220,
            "website": "https://finedgelogistics-demo.com",
            "lead_source": "LinkedIn Prospecting",
            "notes": "Digital freight payment platform expanding operations across South India. High need for operational pipeline visibility.",
            "created_at": now - timedelta(days=30),
            "updated_at": now - timedelta(days=2),
            "last_contacted": now - timedelta(days=3),
            "next_follow_up": now,  # Due Today
            "icp_score": 88.0,
            "priority": "Priority A",
            "pipeline_stage": "Proposal",
            "deal_value": 6200000.0,
            "probability": 0.70,
            "deal_health": "Healthy",
            "bant": {"budget": True, "authority": True, "need": True, "timeline": True, "score": 90.0, "notes": "Timeline < 30 days. VP Operations leading procurement."},
            "activities": [
                {"type": "LinkedIn", "outcome": "InMail Accepted", "notes": "Shared case study on lead qualification efficiency."},
                {"type": "Meeting", "outcome": "Proposal Review", "notes": "Reviewed workflow automation requirements."}
            ]
        },
        {
            "company_name": "HealthPulse Analytics",
            "contact_name": "Dr. Vikram Sethi",
            "title": "Founder & CEO",
            "email": "vikram.sethi@healthpulse-demo.org",
            "phone": "+91 97312 33445",
            "industry": "HealthTech",
            "location": "Whitefield",
            "employee_count": 120,
            "website": "https://healthpulse-demo.org",
            "lead_source": "Inbound Website",
            "notes": "Hospital management SaaS provider. Experiencing high lead leakage between inbound inquiries and discovery calls.",
            "created_at": now - timedelta(days=15),
            "updated_at": now - timedelta(days=1),
            "last_contacted": now - timedelta(days=1),
            "next_follow_up": now + timedelta(days=2),  # Upcoming
            "icp_score": 90.0,
            "priority": "Priority A",
            "pipeline_stage": "Discovery Booked",
            "deal_value": 3800000.0,
            "probability": 0.50,
            "deal_health": "Healthy",
            "bant": {"budget": True, "authority": True, "need": True, "timeline": False, "score": 85.0, "notes": "Budget confirmed, needs 60-day rollout schedule."},
            "activities": [
                {"type": "Inbound", "outcome": "Form Submitted", "notes": "Requested demo for 25 sales associates."}
            ]
        },
        {
            "company_name": "Aegis IT Solutions",
            "contact_name": "Siddharth Nair",
            "title": "Head of Delivery",
            "email": "siddharth.nair@aegisitsolutions-demo.in",
            "phone": "+91 98860 44556",
            "industry": "IT Services",
            "location": "Electronic City",
            "employee_count": 280,
            "website": "https://aegisitsolutions-demo.in",
            "lead_source": "Partner Referral",
            "notes": "IT staffing and managed services provider. Needs unified cold calling script and cadence tracking engine.",
            "created_at": now - timedelta(days=40),
            "updated_at": now - timedelta(days=5),
            "last_contacted": now - timedelta(days=7),
            "next_follow_up": now - timedelta(days=3),  # Overdue
            "icp_score": 86.0,
            "priority": "Priority A",
            "pipeline_stage": "Qualified",
            "deal_value": 5000000.0,
            "probability": 0.35,
            "deal_health": "At Risk",
            "bant": {"budget": True, "authority": True, "need": True, "timeline": True, "score": 88.0, "notes": "Decision pending final CFO signoff."},
            "activities": [
                {"type": "Call", "outcome": "Connected", "notes": "Qualified BANT parameters. Pain point verified."}
            ]
        },
        {
            "company_name": "Kinetix Supply Chain",
            "contact_name": "Priya Sundaram",
            "title": "Head of Operations",
            "email": "priya.sundaram@kinetix-demo.co.in",
            "phone": "+91 96110 55667",
            "industry": "Logistics",
            "location": "Bellandur",
            "employee_count": 190,
            "website": "https://kinetix-demo.co.in",
            "lead_source": "Industry Conference",
            "notes": "Automated warehouse & cold chain platform. Struggling to convert enterprise leads due to lack of SLA tracking.",
            "created_at": now - timedelta(days=20),
            "updated_at": now - timedelta(days=2),
            "last_contacted": now - timedelta(days=4),
            "next_follow_up": now + timedelta(days=1),  # Upcoming
            "icp_score": 89.0,
            "priority": "Priority A",
            "pipeline_stage": "Engaged",
            "deal_value": 7500000.0,
            "probability": 0.20,
            "deal_health": "Healthy",
            "bant": {"budget": True, "authority": True, "need": True, "timeline": True, "score": 85.0, "notes": "Strong need identified for lead scoring engine."},
            "activities": [
                {"type": "Email", "outcome": "Replied to Cadence #2", "notes": "Requested customized product walk-through."}
            ]
        },

        # Priority B / Moderate to Strong Accounts (10)
        {
            "company_name": "OmniServe Business Services",
            "contact_name": "Rohan Deshmukh",
            "title": "Operations Director",
            "email": "rohan.d@omniserve-demo.com",
            "phone": "+91 94480 66778",
            "industry": "Professional Services",
            "location": "HSR Layout",
            "employee_count": 95,
            "website": "https://omniserve-demo.com",
            "lead_source": "LinkedIn Prospecting",
            "notes": "Corporate legal & compliance consulting firm. Seeking light CRM workflow.",
            "created_at": now - timedelta(days=18),
            "updated_at": now - timedelta(days=3),
            "last_contacted": now - timedelta(days=3),
            "next_follow_up": now + timedelta(days=3),
            "icp_score": 76.0,
            "priority": "Priority B",
            "pipeline_stage": "Engaged",
            "deal_value": 2400000.0,
            "probability": 0.20,
            "deal_health": "Healthy",
            "bant": {"budget": True, "authority": True, "need": True, "timeline": False, "score": 75.0, "notes": "Budget confirmed for Q3."}
        },
        {
            "company_name": "PayFlow Technologies",
            "contact_name": "Meera Banerjee",
            "title": "VP Business Operations",
            "email": "meera.b@payflow-demo.in",
            "phone": "+91 98441 77889",
            "industry": "FinTech",
            "location": "Indiranagar",
            "employee_count": 140,
            "website": "https://payflow-demo.in",
            "lead_source": "Outbound Cold Outreach",
            "notes": "B2B vendor payout platform.",
            "created_at": now - timedelta(days=12),
            "updated_at": now - timedelta(days=1),
            "last_contacted": now - timedelta(days=4),
            "next_follow_up": now,  # Due Today
            "icp_score": 82.0,
            "priority": "Priority B",
            "pipeline_stage": "Contacted",
            "deal_value": 3100000.0,
            "probability": 0.10,
            "deal_health": "Healthy",
            "bant": {"budget": False, "authority": True, "need": True, "timeline": False, "score": 60.0, "notes": "Authority clear, evaluating budget availability."}
        },
        {
            "company_name": "DataNexus Systems",
            "contact_name": "Karthik Menon",
            "title": "Business Unit Head",
            "email": "karthik.m@datanexus-demo.com",
            "phone": "+91 97400 88990",
            "industry": "Technology Services",
            "location": "Outer Ring Road",
            "employee_count": 210,
            "website": "https://datanexus-demo.com",
            "lead_source": "Exhibition / Event",
            "notes": "Data analytics consulting for enterprise clients.",
            "created_at": now - timedelta(days=35),
            "updated_at": now - timedelta(days=10),
            "last_contacted": now - timedelta(days=12),
            "next_follow_up": now - timedelta(days=5),  # Overdue
            "icp_score": 79.0,
            "priority": "Priority B",
            "pipeline_stage": "Qualified",
            "deal_value": 4200000.0,
            "probability": 0.35,
            "deal_health": "Stalled",
            "bant": {"budget": True, "authority": True, "need": True, "timeline": False, "score": 75.0, "notes": "Project delayed due to internal restructuring."}
        },
        {
            "company_name": "CloudOps Solutions",
            "contact_name": "Suresh Hedge",
            "title": "Head of Operations",
            "email": "suresh.h@cloudops-demo.net",
            "phone": "+91 99800 99001",
            "industry": "SaaS",
            "location": "Whitefield",
            "employee_count": 110,
            "website": "https://cloudops-demo.net",
            "lead_source": "LinkedIn Prospecting",
            "notes": "DevOps infrastructure monitoring startup.",
            "created_at": now - timedelta(days=8),
            "updated_at": now - timedelta(days=1),
            "last_contacted": now - timedelta(days=2),
            "next_follow_up": now + timedelta(days=4),
            "icp_score": 80.0,
            "priority": "Priority B",
            "pipeline_stage": "Discovery Booked",
            "deal_value": 2800000.0,
            "probability": 0.50,
            "deal_health": "Healthy",
            "bant": {"budget": True, "authority": True, "need": True, "timeline": True, "score": 80.0, "notes": "Discovery meeting booked for next Tuesday."}
        },
        {
            "company_name": "InnoHealth Systems",
            "contact_name": "Divya Krishnan",
            "title": "COO",
            "email": "divya.k@innohealth-demo.org",
            "phone": "+91 98801 12345",
            "industry": "HealthTech",
            "location": "Koramangala",
            "employee_count": 85,
            "website": "https://innohealth-demo.org",
            "lead_source": "Inbound Website",
            "notes": "Telemedicine infrastructure provider.",
            "created_at": now - timedelta(days=22),
            "updated_at": now - timedelta(days=4),
            "last_contacted": now - timedelta(days=5),
            "next_follow_up": now + timedelta(days=1),
            "icp_score": 78.0,
            "priority": "Priority B",
            "pipeline_stage": "Engaged",
            "deal_value": 1900000.0,
            "probability": 0.20,
            "deal_health": "Healthy",
            "bant": {"budget": False, "authority": True, "need": True, "timeline": True, "score": 75.0, "notes": "Needs approval from medical board for budget."}
        },
        {
            "company_name": "LogiNext Platforms",
            "contact_name": "Alok Sharma",
            "title": "Head of Delivery",
            "email": "alok.s@loginext-demo.in",
            "phone": "+91 99160 23456",
            "industry": "Logistics",
            "location": "Outer Ring Road",
            "employee_count": 260,
            "website": "https://loginext-demo.in",
            "lead_source": "Outbound Cold Outreach",
            "notes": "Last-mile fleet management software.",
            "created_at": now - timedelta(days=45),
            "updated_at": now - timedelta(days=8),
            "last_contacted": now - timedelta(days=15),
            "next_follow_up": now - timedelta(days=2),  # Overdue
            "icp_score": 84.0,
            "priority": "Priority B",
            "pipeline_stage": "Proposal",
            "deal_value": 5800000.0,
            "probability": 0.70,
            "deal_health": "At Risk",
            "bant": {"budget": True, "authority": True, "need": True, "timeline": False, "score": 75.0, "notes": "Proposal submitted 2 weeks ago; awaiting feedback."}
        },
        {
            "company_name": "CyberShield Technologies",
            "contact_name": "Nikhil Agarwal",
            "title": "Founder",
            "email": "nikhil.a@cybershield-demo.in",
            "phone": "+91 97390 34567",
            "industry": "SaaS",
            "location": "HSR Layout",
            "employee_count": 65,
            "website": "https://cybershield-demo.in",
            "lead_source": "LinkedIn Prospecting",
            "notes": "Cybersecurity compliance automation for B2B SaaS.",
            "created_at": now - timedelta(days=14),
            "updated_at": now - timedelta(days=3),
            "last_contacted": now - timedelta(days=3),
            "next_follow_up": now + timedelta(days=5),
            "icp_score": 75.0,
            "priority": "Priority B",
            "pipeline_stage": "Contacted",
            "deal_value": 1800000.0,
            "probability": 0.10,
            "deal_health": "Healthy",
            "bant": {"budget": True, "authority": True, "need": False, "timeline": False, "score": 60.0, "notes": "Founder interested, assessing immediate need."}
        },
        {
            "company_name": "BizScale Advisors",
            "contact_name": "Kavita Reddy",
            "title": "VP Business Operations",
            "email": "kavita.r@bizscale-demo.com",
            "phone": "+91 98455 45678",
            "industry": "Professional Services",
            "location": "Indiranagar",
            "employee_count": 75,
            "website": "https://bizscale-demo.com",
            "lead_source": "Partner Referral",
            "notes": "Management consulting for mid-market tech firms.",
            "created_at": now - timedelta(days=50),
            "updated_at": now - timedelta(days=5),
            "last_contacted": now - timedelta(days=5),
            "next_follow_up": now + timedelta(days=2),
            "icp_score": 72.0,
            "priority": "Priority B",
            "pipeline_stage": "Nurture",
            "deal_value": 1500000.0,
            "probability": 0.10,
            "deal_health": "Healthy",
            "bant": {"budget": False, "authority": True, "need": True, "timeline": False, "score": 60.0, "notes": "Nurturing until Q4 budget review."}
        },
        {
            "company_name": "Strikeforce IT Services",
            "contact_name": "Ganesh Bhat",
            "title": "Head of Delivery",
            "email": "ganesh.b@strikeforce-demo.co.in",
            "phone": "+91 99010 56789",
            "industry": "IT Services",
            "location": "Whitefield",
            "employee_count": 195,
            "website": "https://strikeforce-demo.co.in",
            "lead_source": "Outbound Cold Outreach",
            "notes": "Cloud migration and DevOps consultancy.",
            "created_at": now - timedelta(days=28),
            "updated_at": now - timedelta(days=6),
            "last_contacted": now - timedelta(days=6),
            "next_follow_up": now + timedelta(days=1),
            "icp_score": 81.0,
            "priority": "Priority B",
            "pipeline_stage": "Engaged",
            "deal_value": 3600000.0,
            "probability": 0.20,
            "deal_health": "Healthy",
            "bant": {"budget": True, "authority": True, "need": True, "timeline": False, "score": 75.0, "notes": "Needs custom integration with existing ERP."}
        },
        {
            "company_name": "Trident B2B Platform",
            "contact_name": "Deepak Kapoor",
            "title": "COO",
            "email": "deepak.k@tridentb2b-demo.com",
            "phone": "+91 96200 67890",
            "industry": "B2B Platforms",
            "location": "Electronic City",
            "employee_count": 160,
            "website": "https://tridentb2b-demo.com",
            "lead_source": "Industry Conference",
            "notes": "Industrial equipment procurement marketplace.",
            "created_at": now - timedelta(days=16),
            "updated_at": now - timedelta(days=2),
            "last_contacted": now - timedelta(days=2),
            "next_follow_up": now + timedelta(days=3),
            "icp_score": 83.0,
            "priority": "Priority B",
            "pipeline_stage": "Identified",
            "deal_value": 4100000.0,
            "probability": 0.05,
            "deal_health": "Healthy",
            "bant": {"budget": False, "authority": True, "need": True, "timeline": False, "score": 60.0, "notes": "Initial contact planned for this week."}
        },

        # Priority C / Low Probability or Early Pipeline Accounts (13)
        {
            "company_name": "AgileTech Labs",
            "contact_name": "Sanjay Dutt",
            "title": "Founder",
            "email": "sanjay@agiletech-demo.io",
            "phone": "+91 98440 78901",
            "industry": "SaaS",
            "location": "HSR Layout",
            "employee_count": 35,
            "website": "https://agiletech-demo.io",
            "lead_source": "Inbound Website",
            "notes": "Early stage developer tools startup.",
            "created_at": now - timedelta(days=5),
            "updated_at": now - timedelta(days=5),
            "last_contacted": None,
            "next_follow_up": now + timedelta(days=1),
            "icp_score": 58.0,
            "priority": "Priority C",
            "pipeline_stage": "Identified",
            "deal_value": 800000.0,
            "probability": 0.05,
            "deal_health": "Healthy",
            "bant": {"budget": False, "authority": True, "need": False, "timeline": False, "score": 35.0, "notes": "Limited budget."}
        },
        {
            "company_name": "PulseMedia B2B",
            "contact_name": "Neha Joshi",
            "title": "Head of Operations",
            "email": "neha@pulsemedia-demo.in",
            "phone": "+91 97410 89012",
            "industry": "Professional Services",
            "location": "Koramangala",
            "employee_count": 45,
            "website": "https://pulsemedia-demo.in",
            "lead_source": "LinkedIn Prospecting",
            "notes": "Digital marketing agency specializing in B2B tech.",
            "created_at": now - timedelta(days=10),
            "updated_at": now - timedelta(days=4),
            "last_contacted": now - timedelta(days=4),
            "next_follow_up": now + timedelta(days=6),
            "icp_score": 62.0,
            "priority": "Priority C",
            "pipeline_stage": "Contacted",
            "deal_value": 950000.0,
            "probability": 0.10,
            "deal_health": "Healthy",
            "bant": {"budget": False, "authority": True, "need": True, "timeline": False, "score": 50.0, "notes": "Exploring options."}
        },
        {
            "company_name": "Nexus Logistics Solutions",
            "contact_name": "Vikramaditya Paul",
            "title": "Operations Director",
            "email": "vikram@nexuslogistics-demo.com",
            "phone": "+91 99860 90123",
            "industry": "Logistics",
            "location": "Bellandur",
            "employee_count": 310,
            "website": "https://nexuslogistics-demo.com",
            "lead_source": "Outbound Cold Outreach",
            "notes": "Freight forwarding company.",
            "created_at": now - timedelta(days=60),
            "updated_at": now - timedelta(days=20),
            "last_contacted": now - timedelta(days=30),
            "next_follow_up": None,  # No follow-up set
            "icp_score": 68.0,
            "priority": "Priority C",
            "pipeline_stage": "Lost",
            "deal_value": 5200000.0,
            "probability": 0.00,
            "deal_health": "Lost",
            "bant": {"budget": False, "authority": False, "need": False, "timeline": False, "score": 20.0, "notes": "Chose competitor solution due to pre-existing agreement."}
        },
        {
            "company_name": "SmartOps Automation",
            "contact_name": "Tarun Kumar",
            "title": "Business Unit Head",
            "email": "tarun@smartops-demo.in",
            "phone": "+91 96100 01234",
            "industry": "Technology Services",
            "location": "Whitefield",
            "employee_count": 130,
            "website": "https://smartops-demo.in",
            "lead_source": "Exhibition / Event",
            "notes": "RPA implementation partner.",
            "created_at": now - timedelta(days=3),
            "updated_at": now - timedelta(days=1),
            "last_contacted": None,
            "next_follow_up": now + timedelta(days=2),
            "icp_score": 65.0,
            "priority": "Priority C",
            "pipeline_stage": "Identified",
            "deal_value": 1200000.0,
            "probability": 0.05,
            "deal_health": "Healthy",
            "bant": {"budget": False, "authority": True, "need": True, "timeline": False, "score": 45.0, "notes": "Just identified from event attendee list."}
        },
        {
            "company_name": "Beacon Health Systems",
            "contact_name": "Dr. Sunita Murthy",
            "title": "Head of Operations",
            "email": "sunita@beaconhealth-demo.org",
            "phone": "+91 98451 12340",
            "industry": "HealthTech",
            "location": "Indiranagar",
            "employee_count": 150,
            "website": "https://beaconhealth-demo.org",
            "lead_source": "Partner Referral",
            "notes": "Diagnostic lab automation software.",
            "created_at": now - timedelta(days=40),
            "updated_at": now - timedelta(days=12),
            "last_contacted": now - timedelta(days=12),
            "next_follow_up": now - timedelta(days=4),  # Overdue
            "icp_score": 64.0,
            "priority": "Priority C",
            "pipeline_stage": "Nurture",
            "deal_value": 1700000.0,
            "probability": 0.10,
            "deal_health": "Stalled",
            "bant": {"budget": False, "authority": True, "need": True, "timeline": False, "score": 50.0, "notes": "Evaluating budget in next financial year."}
        },
        {
            "company_name": "Elevate FinTech Labs",
            "contact_name": "Arjun Sen",
            "title": "VP Business Operations",
            "email": "arjun@elevatefintech-demo.com",
            "phone": "+91 99002 23401",
            "industry": "FinTech",
            "location": "Koramangala",
            "employee_count": 80,
            "website": "https://elevatefintech-demo.com",
            "lead_source": "LinkedIn Prospecting",
            "notes": "Micro-lending tech backend.",
            "created_at": now - timedelta(days=7),
            "updated_at": now - timedelta(days=2),
            "last_contacted": now - timedelta(days=3),
            "next_follow_up": now + timedelta(days=3),
            "icp_score": 69.0,
            "priority": "Priority C",
            "pipeline_stage": "Contacted",
            "deal_value": 2100000.0,
            "probability": 0.10,
            "deal_health": "Healthy",
            "bant": {"budget": True, "authority": False, "need": True, "timeline": False, "score": 55.0, "notes": "Contact is junior VP; trying to reach COO."}
        },
        {
            "company_name": "Zion IT Infrastructure",
            "contact_name": "Manoj Tiwari",
            "title": "Head of Delivery",
            "email": "manoj@zionit-demo.in",
            "phone": "+91 97313 34012",
            "industry": "IT Services",
            "location": "Electronic City",
            "employee_count": 240,
            "website": "https://zionit-demo.in",
            "lead_source": "Outbound Cold Outreach",
            "notes": "Data center management services.",
            "created_at": now - timedelta(days=30),
            "updated_at": now - timedelta(days=15),
            "last_contacted": now - timedelta(days=15),
            "next_follow_up": now - timedelta(days=7),  # Overdue
            "icp_score": 67.0,
            "priority": "Priority C",
            "pipeline_stage": "Contacted",
            "deal_value": 2900000.0,
            "probability": 0.10,
            "deal_health": "At Risk",
            "bant": {"budget": False, "authority": True, "need": False, "timeline": False, "score": 40.0, "notes": "Cold call made, no response to follow-up email."}
        },
        {
            "company_name": "Prism B2B Connect",
            "contact_name": "Ritu Saxena",
            "title": "COO",
            "email": "ritu@prismb2b-demo.com",
            "phone": "+91 98861 45012",
            "industry": "B2B Platforms",
            "location": "Outer Ring Road",
            "employee_count": 115,
            "website": "https://prismb2b-demo.com",
            "lead_source": "Inbound Website",
            "notes": "Chemical trading B2B marketplace.",
            "created_at": now - timedelta(days=11),
            "updated_at": now - timedelta(days=1),
            "last_contacted": now - timedelta(days=1),
            "next_follow_up": now + timedelta(days=5),
            "icp_score": 66.0,
            "priority": "Priority C",
            "pipeline_stage": "Engaged",
            "deal_value": 1600000.0,
            "probability": 0.20,
            "deal_health": "Healthy",
            "bant": {"budget": False, "authority": True, "need": True, "timeline": False, "score": 55.0, "notes": "Requesting sample cadence scripts."}
        },
        {
            "company_name": "Quantum Cloud Software",
            "contact_name": "Sameer Kulkarni",
            "title": "Founder",
            "email": "sameer@quantumcloud-demo.in",
            "phone": "+91 96111 56012",
            "industry": "SaaS",
            "location": "HSR Layout",
            "employee_count": 40,
            "website": "https://quantumcloud-demo.in",
            "lead_source": "LinkedIn Prospecting",
            "notes": "HR tech employee onboarding software.",
            "created_at": now - timedelta(days=19),
            "updated_at": now - timedelta(days=5),
            "last_contacted": now - timedelta(days=5),
            "next_follow_up": now + timedelta(days=2),
            "icp_score": 61.0,
            "priority": "Priority C",
            "pipeline_stage": "Identified",
            "deal_value": 750000.0,
            "probability": 0.05,
            "deal_health": "Healthy",
            "bant": {"budget": False, "authority": True, "need": False, "timeline": False, "score": 35.0, "notes": "Founder reviewing deck."}
        },
        {
            "company_name": "Vanguard Logistics Hub",
            "contact_name": "Balaji R",
            "title": "Head of Operations",
            "email": "balaji@vanguardhub-demo.com",
            "phone": "+91 94481 67012",
            "industry": "Logistics",
            "location": "Outer Ring Road",
            "employee_count": 175,
            "website": "https://vanguardhub-demo.com",
            "lead_source": "Industry Conference",
            "notes": "Third-party logistics & fulfillment network.",
            "created_at": now - timedelta(days=90),
            "updated_at": now - timedelta(days=10),
            "last_contacted": now - timedelta(days=10),
            "next_follow_up": None,
            "icp_score": 85.0,
            "priority": "Priority A",
            "pipeline_stage": "Won",
            "deal_value": 8500000.0,
            "probability": 1.00,
            "deal_health": "Healthy",
            "bant": {"budget": True, "authority": True, "need": True, "timeline": True, "score": 100.0, "notes": "Contract signed. Onboarding completed successfully!"},
            "activities": [
                {"type": "Stage Change", "outcome": "Moved to Won", "notes": "Closed ₹85L contract for enterprise RevOps platform deployment."}
            ]
        },
        {
            "company_name": "Astra Tech Services",
            "contact_name": "Pooja Hegde",
            "title": "Operations Director",
            "email": "pooja@astratech-demo.in",
            "phone": "+91 98442 78012",
            "industry": "Technology Services",
            "location": "Whitefield",
            "employee_count": 105,
            "website": "https://astratech-demo.in",
            "lead_source": "Outbound Cold Outreach",
            "notes": "IT maintenance outsourcing company.",
            "created_at": now - timedelta(days=14),
            "updated_at": now - timedelta(days=2),
            "last_contacted": now - timedelta(days=2),
            "next_follow_up": now + timedelta(days=4),
            "icp_score": 59.0,
            "priority": "Priority C",
            "pipeline_stage": "Contacted",
            "deal_value": 1100000.0,
            "probability": 0.10,
            "deal_health": "Healthy",
            "bant": {"budget": False, "authority": True, "need": True, "timeline": False, "score": 45.0, "notes": "Initial call completed."}
        },
        {
            "company_name": "Synergy Professional Corp",
            "contact_name": "Harish Chandra",
            "title": "Business Unit Head",
            "email": "harish@synergycorp-demo.com",
            "phone": "+91 97401 89023",
            "industry": "Professional Services",
            "location": "Indiranagar",
            "employee_count": 55,
            "website": "https://synergycorp-demo.com",
            "lead_source": "LinkedIn Prospecting",
            "notes": "Accounting and tax compliance automation.",
            "created_at": now - timedelta(days=4),
            "updated_at": now - timedelta(days=1),
            "last_contacted": None,
            "next_follow_up": now + timedelta(days=1),
            "icp_score": 55.0,
            "priority": "Priority C",
            "pipeline_stage": "Identified",
            "deal_value": 600000.0,
            "probability": 0.05,
            "deal_health": "Healthy",
            "bant": {"budget": False, "authority": False, "need": True, "timeline": False, "score": 30.0, "notes": "New lead assigned."}
        },
        {
            "company_name": "NextGen Software House",
            "contact_name": "Vijay Shankar",
            "title": "COO",
            "email": "vijay@nextgensoftware-demo.io",
            "phone": "+91 99801 90134",
            "industry": "SaaS",
            "location": "Electronic City",
            "employee_count": 135,
            "website": "https://nextgensoftware-demo.io",
            "lead_source": "Outbound Cold Outreach",
            "notes": "Low-code application builder platform.",
            "created_at": now - timedelta(days=26),
            "updated_at": now - timedelta(days=7),
            "last_contacted": now - timedelta(days=7),
            "next_follow_up": now + timedelta(days=3),
            "icp_score": 67.0,
            "priority": "Priority C",
            "pipeline_stage": "Engaged",
            "deal_value": 1400000.0,
            "probability": 0.20,
            "deal_health": "Healthy",
            "bant": {"budget": True, "authority": False, "need": True, "timeline": False, "score": 55.0, "notes": "Engaged on cold call script demo."}
        }
    ]


def seed_database(session=None):
    """
    Populate SQLite database with initial seed data.
    """
    if session is None:
        with get_db() as db_session:
            return _insert_seed_data(db_session)
    else:
        return _insert_seed_data(session)


def _insert_seed_data(session):
    # Check if leads already exist
    existing_count = session.query(Lead).count()
    if existing_count > 0:
        print(f"[SEED] Database already contains {existing_count} leads. Skipping seed.")
        return existing_count

    print("[SEED] Starting demo database population...")
    leads_data = get_fictional_leads_data()
    inserted_leads = 0

    for item in leads_data:
        bant_info = item.pop("bant", {})
        activities_info = item.pop("activities", [])

        # Create Lead record
        lead = Lead(**item)
        session.add(lead)
        session.flush()  # Obtain lead.id

        # Create Qualification record
        qual = Qualification(
            lead_id=lead.id,
            budget_confirmed=bant_info.get("budget", False),
            authority_confirmed=bant_info.get("authority", False),
            need_confirmed=bant_info.get("need", False),
            timeline_confirmed=bant_info.get("timeline", False),
            bant_score=bant_info.get("score", 0.0),
            qualification_notes=bant_info.get("notes", "")
        )
        session.add(qual)

        # Create Pipeline record
        pipe = Pipeline(
            lead_id=lead.id,
            stage=lead.pipeline_stage,
            deal_value=lead.deal_value,
            probability=lead.probability,
            next_action="Follow up with decision maker" if lead.next_follow_up else "Qualify lead",
            next_follow_up=lead.next_follow_up
        )
        session.add(pipe)

        # Create Activity records
        for act in activities_info:
            activity = Activity(
                lead_id=lead.id,
                activity_type=act.get("type", "Note"),
                outcome=act.get("outcome", ""),
                notes=act.get("notes", "")
            )
            session.add(activity)

        # Create initial Note
        note = Note(
            lead_id=lead.id,
            body=f"Account created from source: {lead.lead_source}. Initial ICP Score: {lead.icp_score}.",
            author="BDA Harish"
        )
        session.add(note)

        inserted_leads += 1

    session.commit()
    print(f"[SEED] Successfully seeded {inserted_leads} fictional Bangalore B2B accounts!")
    return inserted_leads


if __name__ == "__main__":
    init_db()
    seed_database()
