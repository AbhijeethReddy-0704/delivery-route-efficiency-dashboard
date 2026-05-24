# Delivery Performance & Route Efficiency Dashboard

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b.svg)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003b57.svg)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-Pytest-success.svg)](#testing)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black.svg)](.github/workflows/ci.yml)

Portfolio-ready logistics analytics project built for third-party delivery and supply chain operations.  
It combines synthetic data engineering, KPI modeling, SQLite analytics views, and an executive Streamlit dashboard designed for route-level decision making.

---

## Live Demo
- Streamlit Cloud: [Add your deployed app URL here](https://share.streamlit.io/)
- Local URL: [http://localhost:8501](http://localhost:8501)
- GitHub Repo: [delivery-route-efficiency-dashboard](https://github.com/AbhijeethReddy-0704/delivery-route-efficiency-dashboard)
- Streamlit Cloud main file path: `streamlit_app.py`

## Project Snapshot
- 120,000 synthetic delivery records
- 30 routes, 18 delivery zones, 7 warehouses, 140 drivers
- Route bottleneck diagnostics and KPI dashboarding
- Synthetic finding: ~12% last-mile SLA improvement opportunity
- Fully local-first: no API keys, no PostgreSQL, no paid services

---

## Table of Contents
1. [Business Context](#business-context)
2. [Solution](#solution)
3. [Dashboard Preview](#dashboard-preview)
4. [Tech Stack](#tech-stack)
5. [Project Structure](#project-structure)
6. [Quick Start](#quick-start)
7. [Dashboard Pages](#dashboard-pages)
8. [KPI Definitions](#kpi-definitions)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Resume Alignment](#resume-alignment)
12. [Notes](#notes)

---

## Business Context
Logistics operations leaders need one place to track:
- SLA attainment and delivery timeliness
- Route-level bottlenecks and delay patterns
- Failure root causes by route/zone
- Driver and vehicle productivity tradeoffs
- Cost efficiency and fuel impact

Without a centralized analytics layer, prioritizing route optimization is slower and less reliable.

## Solution
This project delivers an end-to-end analytics workflow:
1. Generate realistic delivery operations data for 12 months.
2. Validate data quality, schema integrity, and business rules.
3. Build a SQLite analytical model with reusable views.
4. Serve insights via a multi-page Streamlit dashboard with interactive filters.

---

## Dashboard Preview
Visual walkthrough of each dashboard page.

### Executive Overview
![Executive Overview](docs/screenshots/executive_overview.png)

### Route Bottleneck Analysis
![Route Bottleneck Analysis](docs/screenshots/route_bottlenecks.png)

### Delivery Trend Analysis
![Delivery Trend Analysis](docs/screenshots/delivery_trends.png)

### Failure Reason Analysis
![Failure Reason Analysis](docs/screenshots/failure_analysis.png)

### Driver & Vehicle Performance
![Driver and Vehicle Performance](docs/screenshots/driver_vehicle.png)

### Cost & Efficiency Analysis
![Cost and Efficiency Analysis](docs/screenshots/cost_efficiency.png)

### Data Quality & Validation
![Data Quality and Validation](docs/screenshots/data_quality.png)

Screenshot capture guide: `docs/screenshots/SCREENSHOT_GUIDE.md`

---

## Tech Stack
- Python 3.11
- Pandas, NumPy
- SQLite
- Plotly
- Streamlit
- Pytest
- GitHub Actions

## Project Structure
```text
delivery-route-efficiency-dashboard/
|-- data/
|   |-- raw/
|   |-- processed/
|   `-- database/
|-- docs/
|-- scripts/
|-- sql/
|-- src/
|   |-- data/
|   |-- metrics/
|   `-- dashboard/
|-- tests/
|-- .streamlit/
|-- .github/workflows/
`-- streamlit_app.py
```

---

## Quick Start
### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Generate synthetic data
```bash
python scripts/generate_data.py
```

### 3) Validate data
```bash
python scripts/validate_data.py
```
Validation output:
- `data/processed/validation_summary.csv`

### 4) Build SQLite model
```bash
python scripts/build_sqlite_db.py
```

### 5) Run dashboard
```bash
streamlit run streamlit_app.py
```
Open:
```text
http://localhost:8501
```

---

## Dashboard Pages
1. Executive Overview
2. Route Bottleneck Analysis
3. Delivery Trend Analysis
4. Failure Reason Analysis
5. Driver and Vehicle Performance
6. Cost and Efficiency Analysis
7. Data Quality and Validation

Global filters:
- Date range
- Route
- Delivery zone
- Warehouse
- Vehicle type
- Driver
- Customer segment
- Delivery status
- Package priority

---

## KPI Definitions
- SLA attainment rate: `% where sla_met_flag = 1`
- On-time delivery rate: `% where on_time_flag = 1`
- First-attempt success rate: `% where first_attempt_success_flag = 1`
- Failed delivery rate: `% where delivery_status = "Failed"`
- Cost per mile: `sum(delivery_cost) / sum(distance_miles)`
- Route efficiency score: weighted route performance composite
- Improvement opportunity (%): weighted uplift from improving bottom routes to median route SLA

See:
- `docs/KPI_DEFINITIONS.md`
- `docs/SLA_IMPROVEMENT_LOGIC.md`

---

## Testing
Run full checks:
```bash
python -m compileall .
pytest
```

Current coverage scope includes:
- data generation integrity
- KPI calculations
- route bottleneck logic
- SLA opportunity logic
- failure analysis
- SQLite build and SQL views
- dashboard data loading and filter behavior
- validation checks and summary output

---

## Deployment
Detailed guide: `DEPLOYMENT.md`

Streamlit Cloud essentials:
- Repo: `delivery-route-efficiency-dashboard`
- Branch: `main`
- Main file path: `streamlit_app.py`

No PostgreSQL, external APIs, API keys, or secrets required.

---

## Resume Alignment
- Built a logistics performance analytics dashboard tracking delivery productivity KPIs across 100K+ delivery records for a third-party logistics and supply chain environment.
- Visualized delivery trends and bottlenecks across 25+ routes, identifying a 12% improvement opportunity in last-mile SLA attainment and enabling operations leaders to prioritize route optimization and continuous improvement.

---

## Notes
- This is a synthetic dataset and synthetic analytics finding for portfolio demonstration.
- GL is not part of this project; this repository is strictly logistics-focused.
