# SQL Model

## Database
- File: `data/database/delivery_analytics.db`

## Tables
- `deliveries`
- `routes`
- `drivers`
- `warehouses`
- `vehicles`
- `delivery_zones`

## Views
- `vw_daily_delivery_kpis`
- `vw_route_performance`
- `vw_driver_performance`
- `vw_vehicle_efficiency`
- `vw_failure_reason_summary`
- `vw_sla_improvement_opportunity`

## Build Process
`scripts/build_sqlite_db.py`:
1. Executes `sql/schema.sql`
2. Loads `data/processed/delivery_records.csv` into `deliveries`
3. Populates dimension tables (`routes`, `drivers`, `warehouses`, `vehicles`, `delivery_zones`)
4. Executes `sql/views.sql`
5. Validates row-count parity between CSV and `deliveries`
