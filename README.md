# RevOps OS — B2B Lead Intelligence & Revenue Pipeline Platform

> **Product Vision**: A portfolio-grade B2B Revenue Operations platform built for sales execution, lead intelligence, ICP/BANT qualification, outbound cadences, pipeline management, and revenue analytics.

---

## 🎯 Product Purpose

**RevOps OS** centralizes the complete prospect-to-pipeline workflow. Designed specifically to demonstrate high-level Business Development capabilities and software engineering discipline for the **Business Development Associate** role at **Avgova Solutions**.

It bridges business strategy and data engineering by solving critical revenue questions:
- **Who should I contact?** (ICP Scoring & Prospecting)
- **How qualified are they?** (BANT Qualification Engine)
- **What should I say?** (Outreach & Cadence Scripts)
- **When should I follow up?** (Follow-Up Queue & Deal Health Engine)
- **Where is the deal blocking?** (Pipeline Kanban & Funnel Leakage Analytics)

---

## 🏛️ System Architecture

Built using a strict 4-layer decoupled software architecture:

```
                  ┌───────────────────────────────┐
                  │    Streamlit UI Shell         │
                  │ (Executive Dark SaaS Theme)   │
                  └──────────────┬────────────────┘
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │        Service Layer          │
                  │   (Lead, Pipeline, Analytics) │
                  └──────────────┬────────────────┘
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │     Core Business Logic       │
                  │   (ICP, BANT & Health Engine) │
                  └──────────────┬────────────────┘
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │   Data Layer / Persistence    │
                  │  (SQLAlchemy 2.x + SQLite)    │
                  └───────────────────────────────┘
```

---

## 🛠️ Technology Stack

- **Language**: Python 3.10+
- **Frontend / Shell**: Streamlit (Executive Dark Custom CSS Theme)
- **Database / ORM**: SQLite + SQLAlchemy 2.x Declarative Mapping
- **Data & Analytics**: Pandas, Plotly
- **Testing**: Pytest

---

## 🚀 Quick Start Guide

### 1. Clone & Setup Environment
```bash
git clone https://github.com/harishrobin11/RevOps_OS.git
cd RevOps_OS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Initialize & Seed Database
```bash
python data/seed_data.py
```
*Seeds 28 realistic Bangalore B2B tech accounts across SaaS, FinTech, HealthTech, Logistics, IT Services, and Professional Services.*

### 3. Run Automated Unit Tests
```bash
pytest tests/
```

### 4. Launch Application
```bash
streamlit run app.py
```

---

## 📊 Modules & Roadmap

- [x] **Sprint 1 — Foundation & Executive Dashboard**: System configuration, database schema, demo seed generator, executive dark UI design system, app shell, real-time KPI metrics.
- [ ] **Sprint 2 — Data Layer & Service Layer**: Complete CRUD operations for leads, qualifications, activities, and pipelines.
- [ ] **Sprint 3 — Intelligence Engine**: Deterministic Python engines for ICP scoring, BANT qualification, priority weighting, and deal health calculation.
- [ ] **Sprint 4 — Lead Intelligence Module**: Complete registry, multi-criteria filtering, search, sorting, and lead management.
- [ ] **Sprint 5 — Account / Lead Detail CRM View**: 3-column executive deal card view with activity timelines and note logging.
- [ ] **Sprint 6 — Pipeline Management**: Kanban board with stage movement and deal health badges.
- [ ] **Sprint 7 — Outreach & Script Engine**: Multichannel cold calling, email, LinkedIn cadences, and objection handling.
- [ ] **Sprint 8 — Revenue Analytics**: Funnel conversion, stage leakage, industry performance, and at-risk deal analytics.
- [ ] **Sprint 9 — Data Import & Export**: Robust CSV import validation and export engine.
- [ ] **Sprint 10 — UI Polish & E2E Validation**: Refined typography, status badges, empty states, and user experience polish.

---

## 💼 Business Positioning

*Built by Harish Robin H. for Avgova Solutions portfolio demonstration.*
"Designed to help B2B revenue teams prioritize the right accounts, standardize qualification, execute consistent outbound cadences, track next actions, and eliminate sales funnel leakage."
