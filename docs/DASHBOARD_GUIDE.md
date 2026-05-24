# Dashboard Guide

Run:
```bash
streamlit run streamlit_app.py
```

## Visual Design
- Executive-style layout with modern metric cards and insight callouts.
- Page-specific visual patterns (command center, prioritization, time-series, root-cause, operations, financial, audit).
- Interactive Plotly charts and filter-aware analysis on every page.

## Pages
1. **Executive Overview**: KPI command center, SLA opportunity hero card, monthly SLA/volume trends, on-time vs late donut.
2. **Route Bottleneck Analysis**: route leaderboard, top bottlenecks, SLA heatmap, route volume vs SLA bubble chart, route opportunity ranking.
3. **Delivery Trend Analysis**: monthly volume area chart, SLA trend, weekday grouped bars, Monday/Friday vs mid-week comparison, delay and rolling late trends.
4. **Failure Reason Analysis**: failure donut, stacked zone breakdown, route/failure heatmap, address-issue hotspots, customer unavailable trend.
5. **Driver and Vehicle Performance**: top/bottom driver leaderboard, productivity scatter, first-attempt success, vehicle cost/fuel efficiency, heavy vehicle cost impact.
6. **Cost and Efficiency Analysis**: cost trend, route cost-per-mile, fuel by vehicle, distance vs cost scatter, high-cost route ranking, cost opportunity insight.
7. **Data Quality and Validation**: pass/fail cards, row/duplicate/SLA checks, missing values, validation summary table, data freshness note.

## Sidebar Filters
- Date range
- Route
- Delivery zone
- Warehouse
- Vehicle type
- Driver
- Customer segment
- Delivery status
- Package priority

## Notes
- App is local-data based (SQLite/CSV).
- If data is missing, app displays commands to generate/build data.
- No external APIs, secrets, or paid services are required.
