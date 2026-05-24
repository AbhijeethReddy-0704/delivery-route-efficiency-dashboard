# Portfolio Case Study: Delivery Performance & Route Efficiency Dashboard

## Business Context
Third-party logistics teams need a practical decision-support dashboard to monitor SLA attainment, delivery productivity, failure causes, and route-level cost tradeoffs.

## Data Engineering Workflow
1. Generate realistic synthetic delivery operations data (`scripts/generate_data.py`).
2. Validate data quality and business rules (`scripts/validate_data.py`).
3. Build SQLite analytical model with tables and views (`scripts/build_sqlite_db.py`, `sql/schema.sql`, `sql/views.sql`).
4. Serve stakeholder analytics via Streamlit (`streamlit_app.py`, `src/dashboard/*`).

## KPI Calculation Layer
KPI modules in `src/metrics/` calculate operational metrics including SLA attainment, on-time rate, first-attempt success, cost per mile, route efficiency score, and synthetic improvement opportunity.

## Dashboard Design
The dashboard is structured for operational users:
- Executive KPI scan
- Route bottleneck diagnosis
- Trend and seasonality tracking
- Failure driver analysis
- Driver and fleet performance
- Cost and efficiency analysis
- Data quality verification

## Route Bottleneck Methodology
Routes are assessed by SLA attainment, delay minutes, failure rate, and first-attempt success. Composite ranking and threshold logic identify the worst-performing routes and likely bottlenecks.

## SLA Improvement Opportunity Calculation
The model estimates uplift by improving bottom-performing routes to median route SLA performance. This yields an approximate **12% synthetic improvement opportunity** in last-mile SLA attainment.

## Key Findings
- Significant route-to-route performance variance exists across the 25+ route network.
- Bottleneck routes disproportionately drive SLA misses and delay concentration.
- A focused intervention on low-performing routes shows meaningful synthetic SLA uplift potential.

## Technical Challenges
- Balancing realistic scenario generation with deterministic outputs for repeatable testing.
- Maintaining coherent metrics across Python KPI logic, SQLite views, and dashboard visualizations.
- Building fast, reliable tests without sacrificing coverage on a large synthetic dataset.

## Resume Alignment
• Built a logistics performance analytics dashboard tracking delivery productivity KPIs across 100K+ delivery records for a third-party logistics and supply chain environment.
• Visualized delivery trends and bottlenecks across 25+ routes, identifying a 12% improvement opportunity in last-mile SLA attainment and enabling operations leaders to prioritize route optimization and continuous improvement.

## Resume-Ready Bullets
• Built a logistics performance analytics dashboard tracking delivery productivity KPIs across 100K+ delivery records for a third-party logistics and supply chain environment.
• Visualized delivery trends and bottlenecks across 25+ routes, identifying a 12% improvement opportunity in last-mile SLA attainment and enabling operations leaders to prioritize route optimization and continuous improvement.
