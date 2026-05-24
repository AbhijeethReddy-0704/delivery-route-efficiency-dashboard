DROP VIEW IF EXISTS vw_daily_delivery_kpis;
DROP VIEW IF EXISTS vw_route_performance;
DROP VIEW IF EXISTS vw_driver_performance;
DROP VIEW IF EXISTS vw_vehicle_efficiency;
DROP VIEW IF EXISTS vw_failure_reason_summary;
DROP VIEW IF EXISTS vw_sla_improvement_opportunity;

CREATE VIEW vw_daily_delivery_kpis AS
SELECT
    scheduled_delivery_date AS delivery_date,
    COUNT(*) AS total_deliveries,
    ROUND(AVG(on_time_flag) * 100.0, 2) AS on_time_rate,
    ROUND(AVG(sla_met_flag) * 100.0, 2) AS sla_attainment_rate,
    ROUND(AVG(first_attempt_success_flag) * 100.0, 2) AS first_attempt_success_rate,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
    ROUND(AVG(delivery_cost), 2) AS avg_cost_per_delivery
FROM deliveries
GROUP BY scheduled_delivery_date;

CREATE VIEW vw_route_performance AS
SELECT
    route_id,
    route_name,
    COUNT(*) AS delivery_volume,
    ROUND(AVG(sla_met_flag) * 100.0, 2) AS sla_attainment_rate,
    ROUND(AVG(on_time_flag) * 100.0, 2) AS on_time_rate,
    ROUND(AVG(first_attempt_success_flag) * 100.0, 2) AS first_attempt_success_rate,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
    ROUND(AVG(delivery_cost), 2) AS avg_cost_per_delivery,
    ROUND(AVG(CASE WHEN delivery_status = 'Failed' THEN 1.0 ELSE 0.0 END) * 100.0, 2) AS failed_delivery_rate
FROM deliveries
GROUP BY route_id, route_name;

CREATE VIEW vw_driver_performance AS
SELECT
    driver_id,
    COUNT(*) AS deliveries_handled,
    ROUND(AVG(sla_met_flag) * 100.0, 2) AS sla_attainment_rate,
    ROUND(AVG(on_time_flag) * 100.0, 2) AS on_time_rate,
    ROUND(AVG(first_attempt_success_flag) * 100.0, 2) AS first_attempt_success_rate,
    ROUND(AVG(attempt_count), 2) AS avg_attempt_count,
    ROUND(AVG(delivery_cost), 2) AS avg_cost_per_delivery
FROM deliveries
GROUP BY driver_id;

CREATE VIEW vw_vehicle_efficiency AS
SELECT
    vehicle_type,
    COUNT(*) AS delivery_volume,
    ROUND(AVG(sla_met_flag) * 100.0, 2) AS sla_attainment_rate,
    ROUND(AVG(delivery_cost), 2) AS avg_cost_per_delivery,
    ROUND(SUM(delivery_cost) / NULLIF(SUM(distance_miles), 0), 4) AS cost_per_mile,
    ROUND(SUM(distance_miles) / NULLIF(SUM(fuel_consumed_gallons), 0), 2) AS miles_per_gallon
FROM deliveries
GROUP BY vehicle_type;

CREATE VIEW vw_failure_reason_summary AS
SELECT
    failure_reason,
    COUNT(*) AS failure_count,
    ROUND(COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM deliveries WHERE delivery_status = 'Failed'), 0), 2) AS failure_share_pct
FROM deliveries
WHERE delivery_status = 'Failed'
GROUP BY failure_reason;

CREATE VIEW vw_sla_improvement_opportunity AS
WITH route_stats AS (
    SELECT
        route_id,
        route_name,
        COUNT(*) AS delivery_volume,
        AVG(sla_met_flag) * 100.0 AS sla_attainment_rate
    FROM deliveries
    GROUP BY route_id, route_name
),
ranked AS (
    SELECT
        route_id,
        route_name,
        delivery_volume,
        sla_attainment_rate,
        ROW_NUMBER() OVER (ORDER BY sla_attainment_rate ASC) AS rn,
        COUNT(*) OVER () AS total_routes
    FROM route_stats
),
route_median AS (
    SELECT AVG(sla_attainment_rate) AS median_route_sla
    FROM (
        SELECT sla_attainment_rate
        FROM ranked
        ORDER BY sla_attainment_rate
        LIMIT 2 - (SELECT total_routes % 2 FROM ranked LIMIT 1)
        OFFSET (SELECT (total_routes - 1) / 2 FROM ranked LIMIT 1)
    )
),
bottom_routes AS (
    SELECT *
    FROM ranked
    WHERE rn <= (
        SELECT CASE
            WHEN CAST(total_routes * 0.33 AS INTEGER) < 1 THEN 1
            ELSE CAST(total_routes * 0.33 AS INTEGER)
        END
        FROM ranked
        LIMIT 1
    )
),
weighted AS (
    SELECT
        SUM(CASE
            WHEN (SELECT median_route_sla FROM route_median) > sla_attainment_rate
            THEN ((SELECT median_route_sla FROM route_median) - sla_attainment_rate) * delivery_volume
            ELSE 0
        END) / NULLIF((SELECT SUM(delivery_volume) FROM route_stats), 0) AS improvement_opportunity_percentage
    FROM bottom_routes
),
overall AS (
    SELECT AVG(sla_met_flag) * 100.0 AS current_overall_sla_attainment
    FROM deliveries
)
SELECT
    ROUND((SELECT current_overall_sla_attainment FROM overall), 2) AS current_overall_sla_attainment,
    ROUND((SELECT median_route_sla FROM route_median), 2) AS median_route_sla_attainment,
    ROUND((SELECT improvement_opportunity_percentage FROM weighted), 2) AS improvement_opportunity_percentage,
    ROUND(
        (SELECT current_overall_sla_attainment FROM overall)
        + (SELECT improvement_opportunity_percentage FROM weighted),
        2
    ) AS projected_sla_attainment;
