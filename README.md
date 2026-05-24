# Delivery Performance & Route Efficiency Dashboard

A production-style logistics analytics portfolio project for third-party delivery operations, focused on SLA attainment, route bottlenecks, failure root causes, and cost efficiency.

## Business Problem
Operations teams need one place to monitor delivery productivity, SLA misses, route risk, and cost performance across routes, zones, drivers, and vehicle types.

## Solution Overview
- Generate 100K+ realistic synthetic delivery records
- Validate data quality and business rules
- Build a SQLite analytical model with reusable views
- Deliver executive and diagnostic insights in a multi-page Streamlit dashboard

## Dashboard URLs
- Local dashboard URL: `http://localhost:8501`
- Streamlit Cloud URL: `ADD_YOUR_STREAMLIT_CLOUD_URL_HERE`
- GitHub repo URL: `https://github.com/AbhijeethReddy-0704/delivery-route-efficiency-dashboard`

## Quick Visual Preview
Recruiter-friendly snapshots (no app launch needed):

### Executive Overview
![Executive Overview](docs/screenshots/executive_overview.png)

### Route Bottleneck Analysis
![Route Bottleneck Analysis](docs/screenshots/route_bottlenecks.png)

### Delivery Trend Analysis
![Delivery Trend Analysis](docs/screenshots/delivery_trends.png)

### Failure Reason Analysis
![Failure Reason Analysis](docs/screenshots/failure_analysis.png)

### Driver and Vehicle Performance
![Driver and Vehicle Performance](docs/screenshots/driver_vehicle.png)

### Cost and Efficiency Analysis
![Cost and Efficiency Analysis](docs/screenshots/cost_efficiency.png)

### Data Quality and Validation
![Data Quality and Validation](docs/screenshots/data_quality.png)

## Tech Stack
- Python 3.11
- Pandas, NumPy
- SQLite
- Streamlit
- Plotly
- Pytest

## Architecture Overview
- Data generation: `scripts/generate_data.py`
- Validation: `scripts/validate_data.py` -> `data/processed/validation_summary.csv`
- SQL model build: `scripts/build_sqlite_db.py` using `sql/schema.sql` + `sql/views.sql`
- Dashboard app: `streamlit_app.py` + `src/dashboard/*`

## Folder Structure
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

## Setup
```bash
pip install -r requirements.txt
```

## Data Generation
```bash
python scripts/generate_data.py
```

## Build SQLite Database
```bash
python scripts/build_sqlite_db.py
```

## Validate Data
```bash
python scripts/validate_data.py
```

## Run Dashboard
```bash
streamlit run streamlit_app.py
```
Open: `http://localhost:8501`

## Testing
```bash
pytest
```

## Dashboard Pages
1. Executive Overview
2. Route Bottleneck Analysis
3. Delivery Trend Analysis
4. Failure Reason Analysis
5. Driver and Vehicle Performance
6. Cost and Efficiency Analysis
7. Data Quality and Validation

## KPI Definitions (Core)
- SLA attainment rate: `% deliveries where sla_met_flag = 1`
- On-time delivery rate: `% deliveries where on_time_flag = 1`
- First-attempt success rate: `% deliveries where first_attempt_success_flag = 1`
- Failed delivery rate: `% deliveries where delivery_status = "Failed"`
- Cost per mile: `sum(delivery_cost) / sum(distance_miles)`

## Deployment
See `DEPLOYMENT.md` for Streamlit Cloud deployment.

## Screenshot Files
- `docs/screenshots/executive_overview.png`
- `docs/screenshots/route_bottlenecks.png`
- `docs/screenshots/delivery_trends.png`
- `docs/screenshots/failure_analysis.png`
- `docs/screenshots/driver_vehicle.png`
- `docs/screenshots/cost_efficiency.png`
- `docs/screenshots/data_quality.png`
- Capture checklist: `docs/screenshots/SCREENSHOT_GUIDE.md`

## Resume Bullet Alignment
- Built a logistics performance analytics dashboard tracking delivery productivity KPIs across 100K+ delivery records for a third-party logistics and supply chain environment.
- Visualized delivery trends and bottlenecks across 25+ routes, identifying a 12% improvement opportunity in last-mile SLA attainment and enabling operations leaders to prioritize route optimization and continuous improvement.

## Notes
- App defaults to local SQLite/CSV data.
- No PostgreSQL, external APIs, API keys, or paid services are required.
