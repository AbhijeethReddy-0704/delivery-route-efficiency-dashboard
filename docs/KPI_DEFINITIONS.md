# KPI Definitions

- **Total Deliveries**: `count(delivery_id)`
- **SLA Attainment Rate**: `mean(sla_met_flag) * 100`
- **On-Time Delivery Rate**: `mean(on_time_flag) * 100`
- **First-Attempt Success Rate**: `mean(first_attempt_success_flag) * 100`
- **Average Delivery Delay**: `mean(delay_minutes)`
- **Average Cost per Delivery**: `mean(delivery_cost)`
- **Cost per Mile**: `sum(delivery_cost) / sum(distance_miles)`
- **Average Delivery Attempts**: `mean(attempt_count)`
- **Failed Delivery Rate**: `mean(delivery_status == "Failed") * 100`
- **Route Efficiency Score**: weighted composite of SLA, delay, first-attempt success, and cost
- **Driver Productivity Score**: weighted composite of first-attempt success, on-time rate, and attempts
- **Vehicle Utilization Efficiency**: normalized score balancing delivery productivity and fuel intensity
- **Last-Mile SLA Attainment**: `mean(sla_met_flag where last_mile_flag = 1) * 100`
- **Bottleneck Route Count**: number of routes crossing SLA/delay/failure thresholds
- **Improvement Opportunity Percentage**: modeled SLA uplift from improving bottom routes to median SLA
