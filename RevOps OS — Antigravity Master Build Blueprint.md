# REVOPS OS — MASTER BUILD BLUEPRINT

## Project Name

RevOps_Avgova_System

## Product Name

RevOps OS — B2B Lead Intelligence & Revenue Pipeline Platform

## Project Purpose

Build a portfolio-grade B2B Revenue Operations platform that demonstrates how a Business Development Associate can use structured data, qualification frameworks, outreach workflows, pipeline management, and analytics to manage prospects and improve sales execution.

This must NOT look like a basic CRUD application or a college demo.

It should feel like a lightweight internal SaaS product that a real B2B sales/business-development team could use.

The system should demonstrate:

Research → Prospect → Qualify → Engage → Track → Analyze → Improve

The primary portfolio objective is to demonstrate:

- Business development thinking
- Lead intelligence
- Market research
- ICP identification
- BANT qualification
- Sales outreach
- Pipeline discipline
- Follow-up management
- Revenue analytics
- Data-driven decision making
- Software engineering ability
- Dashboard and product thinking

Target role:

Business Development Associate — Avgova Solutions

Candidate:

Harish Robin H.

---

# 1. CORE PRODUCT VISION

RevOps OS centralizes the complete prospect-to-pipeline workflow.

The application should allow a user to:

1. Identify potential B2B accounts
2. Store company and decision-maker information
3. Determine whether the account fits the ICP
4. Score the prospect
5. Qualify the prospect using BANT
6. Generate personalized outreach
7. Execute a structured follow-up cadence
8. Record sales activities
9. Move prospects through a pipeline
10. Track stalled or leaking opportunities
11. Monitor follow-up deadlines
12. Analyze conversion performance
13. Export and import lead data
14. Understand which prospects deserve attention next

The product should answer:

"Who should I contact?"

"Why should I contact them?"

"How qualified are they?"

"What should I say?"

"When should I follow up?"

"Where is this prospect in the pipeline?"

"What is blocking conversion?"

"Which parts of the funnel are performing poorly?"

---

# 2. PRIMARY USER

Primary user:

Business Development Associate / Sales Development Representative / Revenue Operations user.

Typical workflow:

Morning:

- Open dashboard
- Review pipeline health
- Check overdue follow-ups
- Review Priority A accounts
- Identify today's outreach

During prospecting:

- Add a company
- Identify decision maker
- Evaluate ICP fit
- Record pain points
- Assign lead source
- Score account

During qualification:

- Evaluate Budget
- Evaluate Authority
- Evaluate Need
- Evaluate Timeline
- Calculate BANT score
- Assign Priority A/B/C

During outreach:

- Generate cold-call script
- Generate email
- Generate LinkedIn message
- Follow cadence
- Log activity
- Record response

During pipeline management:

- Move opportunity between stages
- Add notes
- Set next action
- Set follow-up date
- Monitor deal health

Management:

- Review funnel
- Analyze conversion
- Identify leakage
- Analyze lead sources
- Analyze industries
- Review activity trends

---

# 3. TARGET ICP

The initial demo ICP should focus on Bangalore-based B2B companies.

Target industries:

- SaaS
- IT Services
- FinTech
- HealthTech
- Logistics
- Professional Services
- Technology Services
- B2B Platforms

Preferred company size:

50–300 employees.

Preferred territories:

- Outer Ring Road
- Whitefield
- Koramangala
- Electronic City
- HSR Layout
- Indiranagar
- Bellandur

Decision-maker personas:

- COO
- VP Business Operations
- Head of Operations
- Head of Delivery
- Operations Director
- Founder
- Business Unit Head

Typical business problems:

- Manual workflows
- Operational bottlenecks
- Poor process visibility
- Scaling challenges
- Repetitive manual work
- Fragmented systems
- Poor reporting
- Inefficient internal processes

Important:

Use fictional companies and fictional contacts for demo data.

Do NOT use real personal contact information.

---

# 4. CORE PRODUCT MODULES

Build the following modules.

## Module 1 — Executive Dashboard

The landing page.

Show:

- Total Accounts
- Contacted Accounts
- Qualified Leads
- Discovery Meetings
- Open Opportunities
- Pipeline Value
- Conversion Rate
- Overdue Follow-ups

Charts:

- Pipeline Funnel
- Pipeline Stage Distribution
- Industry Distribution
- BANT Distribution
- Lead Source Distribution
- Outreach Activity Trend

Also include:

### Priority Accounts

Display the highest-priority accounts with:

Company

Contact

Stage

BANT Score

ICP Score

Priority

Next Action

Follow-up Date

### Follow-up Queue

Show:

- Overdue
- Due Today
- Upcoming

The dashboard should immediately answer:

"What needs my attention today?"

---

# 5. MODULE 2 — LEAD INTELLIGENCE

Create a complete lead registry.

Columns:

- Company
- Contact
- Job Title
- Industry
- Location
- Employees
- Lead Source
- ICP Score
- BANT Score
- Priority
- Pipeline Stage
- Last Contacted
- Next Follow-up
- Created Date

Features:

- Search
- Filter
- Sort
- Pagination where useful
- Industry filter
- Location filter
- Priority filter
- Stage filter
- Lead source filter
- Follow-up status filter

Actions:

- View
- Edit
- Delete
- Qualify
- Generate Outreach
- Move Stage
- Add Activity

---

# 6. MODULE 3 — ACCOUNT / LEAD DETAIL

Create a professional account detail page.

Layout:

LEFT:

Company information

- Company name
- Industry
- Location
- Employee count
- Website
- Lead source
- ICP score

CENTER:

Contact information

- Contact name
- Title
- Email
- Phone
- Decision-maker type

RIGHT:

Qualification summary

- BANT score
- ICP score
- Priority
- Pipeline stage
- Deal health

Below:

Pain Points

Business Context

Notes

Next Action

Next Follow-up

Activity Timeline

The page should feel like a lightweight CRM.

---

# 7. MODULE 4 — ICP SCORING

Create an ICP scoring engine.

Score based on:

Industry fit
Company-size fit
Territory fit
Decision-maker fit
Pain-point fit
Growth/scaling signal

Use a 100-point scoring system.

Recommended weighting:

Industry Fit: 20

Company Size: 15

Territory Fit: 15

Decision Maker Fit: 20

Pain Point Fit: 20

Growth Signal: 10

Total:

100

Classifications:

85–100 = Excellent Fit

70–84 = Strong Fit

50–69 = Moderate Fit

Below 50 = Weak Fit

The scoring logic must be implemented in Python rather than hardcoded in the UI.

---

# 8. MODULE 5 — BANT QUALIFICATION

Implement BANT.

Budget = 25 points

Authority = 35 points

Need = 25 points

Timeline = 15 points

Maximum:

100 points

Qualification rules:

Budget confirmed → +25

Authority confirmed → +35

Need confirmed → +25

Timeline under 90 days → +15

Priority:

85–100:

Priority A / Hot Lead

60–84:

Priority B / Nurture

0–59:

Priority C / Low Probability

Display:

BANT Score

Budget

Authority

Need

Timeline

Priority

Qualification explanation

The user should be able to modify qualification values through the UI.

---

# 9. COMBINED LEAD PRIORITY

Create an overall lead-priority engine.

Combine:

BANT Score

ICP Score

Pipeline Stage

Engagement

Follow-up status

Suggested approach:

Overall Score =
BANT × 0.55
+
ICP × 0.30
+
Engagement × 0.15

Use this only as an initial recommendation.

Clearly display the underlying scores.

Priority:

85+ → Critical

70–84 → High

50–69 → Medium

Below 50 → Low

This should help answer:

"Which lead should I work on first?"

---

# 10. MODULE 6 — PIPELINE MANAGEMENT

Pipeline stages:

1. Identified
2. Contacted
3. Engaged
4. Qualified
5. Discovery Booked
6. Proposal
7. Negotiation
8. Won
9. Lost
10. Nurture

Create a Kanban-style pipeline.

Each card should show:

Company

Contact

Stage

BANT

ICP

Priority

Deal Value

Next Action

Follow-up

Cards should support stage movement.

When stage changes:

- Save to database
- Record activity
- Update timestamp
- Recalculate relevant metrics

---

# 11. DEAL HEALTH

Create deal-health calculation.

Factors:

- Recent activity
- Follow-up status
- Pipeline age
- BANT score
- Engagement
- Stage progression

Health states:

Healthy

At Risk

Stalled

Lost

Display visual status badges.

A stalled lead should be obvious.

---

# 12. MODULE 7 — OUTREACH ENGINE

Create a dedicated Outreach Engine.

Supported channels:

- Cold Call
- Email
- LinkedIn
- Follow-up Call
- Breakup Email

The user selects:

Lead

Channel

Objective

Pain Point

Value Proposition

Tone

Then generate the appropriate message.

Templates should be stored separately from UI code.

Do not build an AI API dependency for the initial version.

Use deterministic template generation.

The architecture should make it easy to replace this later with an LLM.

---

# 13. OUTREACH CADENCE

Default cadence:

DAY 1

Cold Call + LinkedIn

DAY 3

Value-driven Email

DAY 6

Follow-up Call

DAY 9

Permission-to-close-file Email

After Day 9:

Nurture

Each cadence step should contain:

Channel

Objective

Recommended message

Call-to-action

Objection handling

Next action

Allow the user to mark each step:

Pending

Completed

Skipped

Failed

Responded

---

# 14. COLD CALL SCRIPT ENGINE

Generate:

Opening

Reason for calling

Relevant business problem

Discovery question

Value proposition

Qualification question

CTA

Example structure:

"Hi [Name], this is [Rep].

I'm reaching out because we work with businesses dealing with [pain point].

I noticed [company context].

I'm curious — how are you currently handling [workflow]?

If it makes sense, I'd like to understand whether there is an opportunity to improve that process."

Do not make every message identical.

Personalize using lead information.

---

# 15. EMAIL ENGINE

Generate:

Subject

Opening

Relevant company context

Pain point

Value proposition

Proof/benefit

CTA

Signature

Provide multiple tone options:

Professional

Consultative

Concise

Do not generate spammy or exaggerated claims.

---

# 16. LINKEDIN OUTREACH

Generate short messages.

Maximum approximately 300 characters for connection notes.

Use:

Name

Role

Company

Relevant operational context

Simple CTA

---

# 17. OBJECTION HANDLING

Create an objection library.

Initial objections:

"We already have a solution."

"Not interested."

"Send me an email."

"We don't have budget."

"Now isn't a good time."

"We are evaluating internally."

"We already use another provider."

For each objection provide:

Response

Follow-up question

Recommended next action

---

# 18. MODULE 8 — ACTIVITY TIMELINE

Every lead should have an activity timeline.

Activity types:

Call

Email

LinkedIn

Meeting

Note

Stage Change

Qualification

Follow-up

System Event

Each record:

Timestamp

Type

Outcome

Notes

User

Display chronologically.

Newest first.

---

# 19. MODULE 9 — FOLLOW-UP MANAGEMENT

Every active lead should have:

Last Contacted

Next Follow-up

Follow-up Status

Next Action

Follow-up priority

Statuses:

Overdue

Due Today

Upcoming

No Follow-up

Create a dedicated follow-up queue.

---

# 20. MODULE 10 — ANALYTICS

Create a dedicated analytics page.

Metrics:

Total Leads

Contact Rate

Engagement Rate

Qualification Rate

Discovery Conversion

Proposal Conversion

Win Rate

Average Pipeline Age

Average BANT Score

Average ICP Score

Charts:

1. Funnel conversion
2. Stage distribution
3. Industry distribution
4. Lead-source distribution
5. BANT distribution
6. Activity trend
7. Conversion by industry
8. Conversion by lead source
9. Pipeline value by stage
10. Follow-up status

Every chart must answer a business question.

Example:

"Where are prospects dropping out?"

"Which industries produce the strongest leads?"

"Which sources generate qualified opportunities?"

"How much pipeline is at risk?"

---

# 21. MODULE 11 — IMPORT / EXPORT

Implement CSV import.

Required fields:

Company

Contact

Title

Email

Phone

Industry

Location

Employees

Lead Source

Notes

Validate:

Missing company

Invalid email

Duplicate company/contact

Invalid employee count

Invalid dates

Provide clear error messages.

Export:

CSV

Allow exporting:

All leads

Filtered leads

Pipeline

Activities

---

# 22. DATABASE ARCHITECTURE

Use:

SQLite

SQLAlchemy 2.x

Create these core entities.

## Lead

id

company_name

contact_name

title

email

phone

industry

location

employee_count

website

lead_source

notes

created_at

updated_at

last_contacted

next_follow_up

icp_score

priority

pipeline_stage

deal_value

probability

deal_health

## Qualification

id

lead_id

budget_confirmed

authority_confirmed

need_confirmed

timeline_confirmed

bant_score

qualification_notes

updated_at

## Activity

id

lead_id

activity_type

outcome

notes

created_at

## Outreach

id

lead_id

channel

cadence_step

subject

content

status

sent_at

response

## Pipeline

id

lead_id

stage

deal_value

probability

next_action

next_follow_up

entered_stage_at

## Note

id

lead_id

body

created_at

author

Use foreign keys and relationships.

Use indexes where appropriate.

Use timestamps consistently.

Do not use deprecated datetime.utcnow() patterns.

---

# 23. PROJECT ARCHITECTURE

Use this exact structure:

RevOps_Avgova_System/

├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── config.py
│
├── core/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── qualification.py
│   ├── scoring.py
│   ├── analytics.py
│   ├── cadence.py
│   └── templates.py
│
├── services/
│   ├── __init__.py
│   ├── lead_service.py
│   ├── qualification_service.py
│   ├── outreach_service.py
│   ├── pipeline_service.py
│   ├── activity_service.py
│   └── analytics_service.py
│
├── ui/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── leads.py
│   ├── lead_detail.py
│   ├── pipeline.py
│   ├── outreach.py
│   ├── analytics.py
│   ├── settings.py
│   └── components.py
│
├── data/
│   ├── pipeline.db
│   └── seed_data.py
│
├── tests/
│   ├── test_scoring.py
│   ├── test_qualification.py
│   ├── test_leads.py
│   └── test_pipeline.py
│
└── assets/
    └── README.md

IMPORTANT:

Do not put the entire application into app.py.

app.py should primarily handle:

Navigation

Application initialization

Page routing

Global configuration

---

# 24. SERVICE LAYER

The UI must not directly contain database business logic.

Use:

UI

↓

Service Layer

↓

Business Logic

↓

Database

For example:

ui/leads.py

calls

services/lead_service.py

which uses

core/models.py

and

core/database.py

This separation is mandatory.

---

# 25. TECHNOLOGY STACK

Use:

Python 3.10+

Streamlit

SQLAlchemy 2.x

SQLite

Pandas

Plotly

Python standard library

Recommended:

pytest

Do NOT add unnecessary dependencies.

requirements.txt should contain only required packages.

---

# 26. UI/UX DESIGN SYSTEM

The application must look like a premium internal SaaS product.

Design direction:

Modern

Professional

Minimal

Data-dense but readable

Executive

Enterprise

Avoid:

Huge text

Excessive gradients

Cartoon graphics

Overuse of icons

Random colors

Unnecessary animations

Generic Streamlit appearance

Use:

Dark executive interface

Deep navy/slate backgrounds

Slightly lighter cards

Restrained blue primary accent

Green = positive

Amber = warning

Red = critical

Muted gray secondary information

Typography:

Use a modern system sans-serif.

Hierarchy:

Page title

Section title

Card title

Metric

Supporting text

Use:

8–12px border radius

Consistent spacing

Strong alignment

Subtle borders

Minimal shadows

Compact tables

Clear status badges

---

# 27. APPLICATION SHELL

Desktop layout:

SIDEBAR

RevOps OS logo

Dashboard

Leads

Pipeline

Outreach

Analytics

Settings

Bottom:

System status

Database status

Version

MAIN CONTENT

Page header

Breadcrumb/context

Primary actions

Content

SIDEBAR WIDTH:

Approximately 220–250px.

Main content should use the available width efficiently.

---

# 28. DASHBOARD UI WIREFRAME

Build this visual structure:

┌─────────────────────────────────────────────────────────────┐
│ RevOps OS                              Search     Profile   │
├──────────────┬──────────────────────────────────────────────┤
│              │ Executive Dashboard                          │
│ Dashboard    │ Revenue Operations Overview                  │
│ Leads        │                                              │
│ Pipeline     │ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │
│ Outreach     │ │128     │ │74%     │ │42      │ │18      │ │
│ Analytics    │ │Accounts│ │Contact │ │Qualified│ │Meetings│ │
│ Settings     │ └────────┘ └────────┘ └────────┘ └────────┘ │
│              │                                              │
│              │ ┌────────────────────┐ ┌───────────────────┐ │
│              │ │ Pipeline Funnel    │ │ Industry Mix      │ │
│              │ │                    │ │                   │ │
│              │ │ ███████████        │ │ SaaS       32%    │ │
│              │ │ ████████           │ │ IT         27%    │ │
│              │ │ █████              │ │ FinTech    18%    │ │
│              │ │ ███                │ │ Logistics  12%    │ │
│              │ └────────────────────┘ └───────────────────┘ │
│              │                                              │
│              │ ┌───────────────────────────────────────────┐ │
│              │ │ Priority Accounts                         │ │
│              │ │ Company | Score | Stage | Next Action    │ │
│              │ └───────────────────────────────────────────┘ │
└──────────────┴──────────────────────────────────────────────┘

Do not copy this ASCII literally.

Use it as layout guidance.

---

# 29. LEAD DETAIL UI

Create:

Header:

Company Name

Priority Badge

Pipeline Stage

Actions

Then three information cards:

Company Intelligence

Contact Intelligence

Qualification

Then:

Pain Points

Business Context

Next Action

Activity Timeline

Outreach History

Recommended Next Step

The page should resemble a lightweight modern CRM.

---

# 30. PIPELINE UI

Kanban columns:

IDENTIFIED

CONTACTED

ENGAGED

QUALIFIED

DISCOVERY

PROPOSAL

NEGOTIATION

WON

LOST

Each card:

Company

Contact

Priority

BANT

ICP

Deal Value

Next Follow-up

Cards should remain compact.

Provide stage filters.

---

# 31. OUTREACH UI

Top:

Select Lead

Select Channel

Select Cadence Step

Then:

Generated Message

Actions:

Copy

Regenerate

Edit

Log Activity

Mark Completed

Below:

Cadence Timeline

Day 1

Day 3

Day 6

Day 9

---

# 32. ANALYTICS UI

Top KPI row.

Second section:

Funnel

Pipeline Value

Third section:

Industry

Lead Source

Fourth:

Activity Trend

Fifth:

Conversion Analysis

Sixth:

At-Risk Pipeline

The analytics page should feel like a management dashboard.

---

# 33. STREAMLIT UX RULES

Avoid excessive st.columns nesting.

Avoid giant forms.

Use tabs only when useful.

Use expanders for secondary details.

Use dialogs where appropriate if supported by installed Streamlit version.

Use session state carefully.

Do not store business data only in session state.

Database is the source of truth.

After mutations:

Refresh/reload relevant data.

Never require a full application restart after creating a lead.

---

# 34. DEMO DATA

Create approximately 30 fictional Bangalore accounts.

Industries:

SaaS

IT Services

FinTech

HealthTech

Logistics

Professional Services

Create realistic distribution:

5 Priority A

10 Priority B

15 Priority C

Include:

Different pipeline stages

Different BANT scores

Different ICP scores

Different activity histories

Different lead sources

Overdue follow-ups

Upcoming follow-ups

Stalled opportunities

Discovery meetings

Proposals

Won/Lost examples

Use realistic but fictional names.

---

# 35. ERROR HANDLING

The application must never crash because of normal user mistakes.

Handle:

Invalid email

Missing company name

Duplicate lead

Invalid date

Database error

Empty database

Missing data

Malformed CSV

Invalid score

Invalid stage

Show user-friendly messages.

Do not expose raw Python stack traces in normal UI.

---

# 36. EMPTY STATES

Every major page needs a meaningful empty state.

Examples:

"No leads yet."

"Your pipeline is empty."

"No overdue follow-ups."

"No outreach activity recorded."

"No analytics available yet."

Provide an action where appropriate:

Add Lead

Import CSV

Create Activity

---

# 37. SECURITY / DATA QUALITY

For this portfolio version:

- Validate all user inputs
- Use SQLAlchemy ORM
- Avoid raw SQL where unnecessary
- Do not hardcode credentials
- Do not store secrets in source code
- Add .gitignore
- Never include real personal information in demo data
- Keep configuration separate
- Use parameterized database operations

---

# 38. TESTING

Create tests for:

BANT calculation

BANT thresholds

ICP calculation

Priority calculation

Lead creation

Lead validation

Duplicate handling

Pipeline movement

Deal health

Analytics calculations

CSV validation

Follow-up logic

Example:

test_bant_score()

test_priority_tier()

test_icp_score()

test_pipeline_transition()

---

# 39. REQUIREMENTS.TXT

Start with:

streamlit

pandas

plotly

sqlalchemy

pytest

Pin sensible minimum versions rather than blindly installing everything.

---

# 40. README

README must explain:

Product

Problem

Solution

Features

Architecture

Tech stack

Screenshots section

Installation

Running locally

Database

Demo data

Testing

Project structure

Business workflow

Portfolio relevance

Future enhancements

---

# 41. FUTURE ARCHITECTURE

Design the application so future versions could add:

LLM-powered personalization

Real CRM integrations

HubSpot integration

Salesforce integration

Email APIs

LinkedIn workflows

Lead enrichment

Company intelligence APIs

Predictive lead scoring

AI-generated call summaries

AI-powered next-best-action

Multi-user authentication

Role-based access

Cloud PostgreSQL

Background jobs

Production deployment

Do NOT implement these now unless explicitly requested.

Build the architecture so they can be added later.

---

# 42. DEVELOPMENT PHASES

Build in these phases.

## SPRINT 1 — FOUNDATION

Create:

Project structure

Virtual environment compatibility

requirements.txt

config.py

database.py

models.py

DB initialization

Seed system

Basic app shell

Basic navigation

Acceptance:

Application launches successfully.

Database initializes.

Demo data loads.

Navigation works.

---

## SPRINT 2 — DATA LAYER

Implement:

Lead CRUD

Qualification CRUD

Activity CRUD

Pipeline CRUD

Outreach CRUD

Notes

Relationships

Validation

Acceptance:

Data persists across application restarts.

---

## SPRINT 3 — INTELLIGENCE ENGINE

Implement:

BANT

ICP

Priority

Deal Health

Follow-up status

Next action

Unit tests

Acceptance:

Scores are calculated by business logic.

---

## SPRINT 4 — EXECUTIVE DASHBOARD

Implement:

KPI cards

Funnel

Industry chart

Priority accounts

Follow-up queue

Pipeline health

Activity trend

Acceptance:

All dashboard metrics come from database data.

---

## SPRINT 5 — LEAD INTELLIGENCE

Implement:

Lead registry

Search

Filters

Lead creation

Lead editing

Lead detail

Timeline

Notes

Acceptance:

Complete lead workflow works end-to-end.

---

## SPRINT 6 — PIPELINE

Implement:

Kanban

Stage movement

Deal value

Probability

Deal health

Next action

Follow-up

Activity logging

Acceptance:

Moving a lead updates database and analytics.

---

## SPRINT 7 — OUTREACH ENGINE

Implement:

Cold calls

Emails

LinkedIn

Cadence

Objections

Activity logging

Copy/edit actions

Acceptance:

User can select a lead and generate outreach.

---

## SPRINT 8 — ANALYTICS

Implement:

Conversion funnel

Stage leakage

BANT distribution

Industry performance

Source performance

Activity trends

Pipeline value

At-risk opportunities

Acceptance:

Analytics are actionable rather than decorative.

---

## SPRINT 9 — IMPORT / EXPORT

Implement:

CSV import

Validation

Duplicate detection

CSV export

Filtered export

Acceptance:

Users can safely move data in and out.

---

## SPRINT 10 — UI POLISH

Improve:

Spacing

Typography

Cards

Tables

Status badges

Responsive layout

Empty states

Loading states

Error states

Navigation

Accessibility

Acceptance:

Application looks like a professional SaaS dashboard.

---

## SPRINT 11 — QA / DEMO

Perform:

End-to-end testing

Fresh installation

Database reset

Seed verification

Edge-case testing

Demo data validation

Performance review

Fix all obvious UI/runtime errors.

---

## SPRINT 12 — PORTFOLIO

Create:

README

Architecture diagram

Screenshots

Demo walkthrough

Interview explanation

Business case

Technical defense

Deployment configuration

Final cleanup

---

# 43. DEVELOPMENT RULES FOR ANTIGRAVITY

IMPORTANT.

Before modifying code:

1. Inspect the existing repository.
2. Understand current architecture.
3. Do not overwrite working functionality unnecessarily.
4. Follow the existing project structure.
5. Reuse components.
6. Avoid duplicate logic.
7. Keep business logic outside UI.
8. Use type hints.
9. Add validation.
10. Add error handling.
11. Keep functions reasonably small.
12. Use meaningful names.
13. Keep database logic centralized.
14. Keep UI components reusable.
15. Do not create unnecessary dependencies.
16. Do not fabricate functionality.
17. Do not leave placeholder buttons that do nothing.
18. Every visible action must either work or be clearly marked as unavailable.
19. Run tests after meaningful changes.
20. Run the application after UI changes.
21. Fix errors before declaring the sprint complete.

---

# 44. IMPORTANT ANTIGRAVITY BEHAVIOR

Do NOT attempt to implement all 12 sprints at once.

Start with Sprint 1 only.

After Sprint 1:

- Show what was created
- Explain files
- Run validation
- Start Streamlit
- Verify navigation
- Verify database
- Verify seed data
- Fix errors

Then stop.

Wait for the next sprint instruction.

Do not jump ahead.

---

# 45. FIRST IMPLEMENTATION TASK

BEGIN NOW WITH SPRINT 1.

Create:

RevOps_Avgova_System/

├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── config.py
│
├── core/
│   ├── __init__.py
│   ├── database.py
│   └── models.py
│
├── services/
│   └── __init__.py
│
├── ui/
│   ├── __init__.py
│   └── components.py
│
├── data/
│   └── seed_data.py
│
├── tests/
│   └── __init__.py
│
└── assets/
    └── README.md

Implement:

1. Application configuration
2. SQLite database
3. SQLAlchemy engine
4. SQLAlchemy Base
5. Initial Lead model
6. Initial Qualification model
7. Initial Activity model
8. Initial Pipeline model
9. Initial Outreach model
10. Initial Note model
11. Relationships
12. Database initialization
13. Demo seed data
14. Streamlit application shell
15. Sidebar navigation
16. Premium visual foundation
17. Dashboard placeholder with real database counts

Do not implement advanced functionality yet.

---

# 46. INITIAL DATABASE MODEL

Use SQLAlchemy 2.x declarative style.

Lead must support:

id

company_name

contact_name

title

email

phone

industry

location

employee_count

website

lead_source

notes

created_at

updated_at

last_contacted

next_follow_up

icp_score

priority

pipeline_stage

deal_value

probability

deal_health

Qualification must support:

id

lead_id

budget_confirmed

authority_confirmed

need_confirmed

timeline_confirmed

bant_score

qualification_notes

updated_at

Activity:

id

lead_id

activity_type

outcome

notes

created_at

Outreach:

id

lead_id

channel

cadence_step

subject

content

status

sent_at

response

Pipeline:

id

lead_id

stage

deal_value

probability

next_action

next_follow_up

entered_stage_at

Note:

id

lead_id

body

created_at

author

---

# 47. INITIAL DEMO DATA

Seed at least 20 fictional leads.

Use companies such as fictional names resembling realistic B2B organizations.

Do not use real companies or real personal contact details.

Include varied:

Industries

Employee counts

BANT scores

ICP scores

Pipeline stages

Lead sources

Priorities

Follow-up dates

Deal values

---

# 48. INITIAL DASHBOARD

The first dashboard should already show:

Total Accounts

Qualified Leads

Priority A Leads

Open Opportunities

Pipeline Value

Overdue Follow-ups

Use real database queries.

Do not hardcode these numbers.

---

# 49. VISUAL QUALITY REQUIREMENT

The first screen must NOT look like default Streamlit.

Create:

Professional sidebar

Page header

KPI cards

Status badges

Consistent spacing

Dark executive visual theme

Subtle borders

Clean typography

Professional charts when applicable

Use CSS carefully through Streamlit.

Avoid excessive decoration.

---

# 50. VALIDATION AFTER IMPLEMENTATION

After coding:

1. Check Python syntax.
2. Check imports.
3. Initialize database.
4. Seed database.
5. Run tests.
6. Launch Streamlit.
7. Verify all sidebar pages load.
8. Verify KPI counts.
9. Verify database persistence.
10. Fix every runtime error you encounter.

Do not simply tell me that the application should work.

Actually validate it.

---

# 51. FINAL RESPONSE AFTER SPRINT 1

When Sprint 1 is complete, report:

### Files Created

List every file.

### Database

Explain tables and relationships.

### Demo Data

Explain how many records were inserted.

### UI

Explain the current dashboard and navigation.

### Validation

Report:

Syntax check

Import check

Database check

Seed check

Test result

Application launch result

### Next Sprint

Recommend Sprint 2 only.

Do NOT implement Sprint 2 yet.

---

# 52. PRODUCT POSITIONING

Throughout the project, use the product language:

"Revenue Operations Platform"

"Lead Intelligence"

"Pipeline Management"

"Sales Workflow"

"Qualification Engine"

"Outreach Automation"

"Revenue Analytics"

Avoid repeatedly calling it:

"student project"

"college project"

"CRUD app"

"Streamlit project"

The final product should communicate:

"I understand a business process, I can model it as a software system, and I can measure its outcome."

---

# 53. FINAL PORTFOLIO STATEMENT

The final README and portfolio should eventually be able to describe the project as:

"Built a lightweight B2B RevOps platform that centralizes lead intelligence, ICP and BANT qualification, outbound cadences, pipeline management, follow-up workflows and revenue analytics."

Technical positioning:

"Designed a layered Python application using Streamlit, SQLAlchemy, SQLite, Pandas and Plotly with separated UI, service, business-logic and persistence layers."

Business positioning:

"Designed to help B2B teams prioritize the right accounts, standardize qualification, execute consistent outreach, track next actions and identify funnel leakage."

---

# 54. BEGIN

You are now the lead software engineer for this project.

Do not give me a generic tutorial.

Inspect the project environment and BUILD it.

Start with Sprint 1.

Create the complete foundation described above.

Validate it.

Run it.

Fix errors.

Then stop and report the results.