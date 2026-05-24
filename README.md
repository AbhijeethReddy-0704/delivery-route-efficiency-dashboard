# Delivery Performance & Route Efficiency Dashboard

A production-style logistics analytics portfolio project that simulates third-party delivery operations and surfaces route-level performance bottlenecks, SLA risk, and cost efficiency opportunities.

## Professional Summary
This project provides an end-to-end local analytics workflow: synthetic data engineering (100K+ records), KPI computation, SQLite analytical modeling, validation automation, and an interactive Streamlit dashboard for operations leaders.

## Business Problem
Logistics teams need clear visibility into route performance, late-delivery patterns, failure drivers, and cost tradeoffs across warehouses, zones, drivers, and vehicle types. Without a unified analytical view, improvement opportunities in last-mile SLA performance are hard to prioritize.

## Solution Overview
- Generate realistic 12-month delivery operations data.
- Validate data quality and business rules with reproducible checks.
- Build a SQLite analytics layer with curated views.
- Serve executive and diagnostic insights through a multi-page Streamlit dashboard.

## Key Features
- 120,000 synthetic delivery records across 30 routes, 18 zones, 7 warehouses, and 140 drivers.
- KPI layer for SLA attainment, on-time rate, failure rate, route efficiency, and cost metrics.
- Bottleneck route detection and synthetic SLA uplift analysis (~12% opportunity).
- Streamlit dashboard with filters, trend analysis, failure diagnostics, and data quality checks.
- Fully local stack (no APIs, no secrets, no paid services).
- GL is not part of this project; this implementation is strictly logistics-focused.

## Tech Stack
- Python 3.11
- Pandas, NumPy
- SQLite
- Plotly
- Streamlit
- Pytest

## Architecture Overview
- Data generation: `scripts/generate_data.py`
- Validation and quality output: `scripts/validate_data.py` -> `data/processed/validation_summary.csv`
- SQL model build: `scripts/build_sqlite_db.py` using `sql/schema.sql` + `sql/views.sql`
- Dashboard app: `streamlit_app.py` + `src/dashboard/*`

See also: [Architecture Doc](/C:/Users/abhij/delivery-route-efficiency-dashboard/docs/ARCHITECTURE.md)

## Folder Structure
```text
delivery-route-efficiency-dashboard/
├── data/
│   ├── raw/
│   ├── processed/
│   └── database/
├── docs/
├── scripts/
├── sql/
├── src/
│   ├── data/
│   ├── metrics/
│   └── dashboard/
├── tests/
├── .streamlit/
├── .github/workflows/
└── streamlit_app.py
```

## Setup
```bash
pip install -r requirements.txt
```

## Data Generation
```bash
python scripts/generate_data.py
```

## SQLite Database Build
```bash
python scripts/build_sqlite_db.py
```

## Validation
```bash
python scripts/validate_data.py
```
Validation summary output:
- `data/processed/validation_summary.csv`

## Run Dashboard
```bash
streamlit run streamlit_app.py
```

Dashboard experience highlights:
- Modern executive command-center layout with styled KPI cards and insight panels.
- Distinct visual design and analysis purpose per page (executive, bottlenecks, trends, root-cause, operations, financial, audit).
- Interactive Plotly visuals with cross-page filter behavior.

## Testing
```bash
pytest
```

## Deployment
See [DEPLOYMENT.md](/C:/Users/abhij/delivery-route-efficiency-dashboard/DEPLOYMENT.md) for Streamlit Cloud and container deployment guidance.

## KPI Definitions (Core)
- SLA attainment rate: `% deliveries where sla_met_flag = 1`
- On-time delivery rate: `% deliveries where on_time_flag = 1`
- First-attempt success rate: `% deliveries where first_attempt_success_flag = 1`
- Failed delivery rate: `% deliveries where delivery_status = "Failed"`
- Cost per mile: `sum(delivery_cost) / sum(distance_miles)`
- Route efficiency score: weighted composite from SLA, delay, first-attempt success, and cost

See full definitions: [KPI Definitions](/C:/Users/abhij/delivery-route-efficiency-dashboard/docs/KPI_DEFINITIONS.md)

## Screenshot Placeholders
- `docs/screenshots/executive_overview.png`
- `docs/screenshots/route_bottlenecks.png`
- `docs/screenshots/failure_analysis.png`
- `docs/screenshots/cost_efficiency.png`

## Portfolio Impact Summary
- Demonstrates hands-on capability across analytics engineering, SQL modeling, KPI design, and BI storytelling in a logistics domain.
- Shows reproducible, test-driven workflow suitable for production-style data applications.

## Resume Bullet Alignment
• Built a logistics performance analytics dashboard tracking delivery productivity KPIs across 100K+ delivery records for a third-party logistics and supply chain environment.
• Visualized delivery trends and bottlenecks across 25+ routes, identifying a 12% improvement opportunity in last-mile SLA attainment and enabling operations leaders to prioritize route optimization and continuous improvement.

## Future Improvements
- Add scenario planning controls for SLA target changes and route rebalancing.
- Add dashboard export packs for weekly operations reviews.
- Add anomaly detection for sudden route-level degradation.
