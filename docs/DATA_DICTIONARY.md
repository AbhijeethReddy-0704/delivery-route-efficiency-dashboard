# Data Dictionary

Primary dataset: `data/processed/delivery_records.csv`

| Column | Description |
|---|---|
| delivery_id | Unique delivery record ID |
| route_id | Route identifier |
| route_name | Route display name |
| warehouse_id | Warehouse identifier |
| delivery_zone | Delivery zone |
| driver_id | Driver identifier |
| vehicle_type | Vehicle category |
| customer_segment | Customer segment |
| scheduled_delivery_date | Planned delivery date |
| actual_delivery_date | Actual delivery completion date |
| scheduled_delivery_time | Planned delivery time |
| actual_delivery_time | Actual delivery time |
| delivery_status | Delivered On Time / Delivered Late / Failed |
| sla_target_minutes | SLA target in minutes |
| actual_delivery_minutes | Actual end-to-end delivery duration |
| distance_miles | Delivery distance in miles |
| fuel_consumed_gallons | Fuel consumed |
| delivery_cost | Delivery cost |
| attempt_count | Number of attempts |
| first_attempt_success_flag | 1 if first attempt succeeded, else 0 |
| on_time_flag | 1 if on-time under policy window, else 0 |
| sla_met_flag | 1 if SLA target met, else 0 |
| delay_minutes | Minutes beyond SLA target |
| failure_reason | Failure reason or "None" |
| weather_condition | Weather condition |
| traffic_condition | Traffic condition |
| package_priority | Priority band |
| last_mile_flag | 1 if last-mile tagged, else 0 |
