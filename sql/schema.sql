DROP TABLE IF EXISTS deliveries;
DROP TABLE IF EXISTS routes;
DROP TABLE IF EXISTS drivers;
DROP TABLE IF EXISTS warehouses;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS delivery_zones;

CREATE TABLE deliveries (
    delivery_id TEXT PRIMARY KEY,
    route_id TEXT NOT NULL,
    route_name TEXT NOT NULL,
    warehouse_id TEXT NOT NULL,
    delivery_zone TEXT NOT NULL,
    driver_id TEXT NOT NULL,
    vehicle_type TEXT NOT NULL,
    customer_segment TEXT NOT NULL,
    scheduled_delivery_date TEXT NOT NULL,
    actual_delivery_date TEXT NOT NULL,
    scheduled_delivery_time TEXT NOT NULL,
    actual_delivery_time TEXT NOT NULL,
    delivery_status TEXT NOT NULL,
    sla_target_minutes INTEGER NOT NULL,
    actual_delivery_minutes REAL NOT NULL,
    distance_miles REAL NOT NULL,
    fuel_consumed_gallons REAL NOT NULL,
    delivery_cost REAL NOT NULL,
    attempt_count INTEGER NOT NULL,
    first_attempt_success_flag INTEGER NOT NULL,
    on_time_flag INTEGER NOT NULL,
    sla_met_flag INTEGER NOT NULL,
    delay_minutes REAL NOT NULL,
    failure_reason TEXT NOT NULL,
    weather_condition TEXT NOT NULL,
    traffic_condition TEXT NOT NULL,
    package_priority TEXT NOT NULL,
    last_mile_flag INTEGER NOT NULL
);

CREATE TABLE routes (
    route_id TEXT PRIMARY KEY,
    route_name TEXT NOT NULL
);

CREATE TABLE drivers (
    driver_id TEXT PRIMARY KEY
);

CREATE TABLE warehouses (
    warehouse_id TEXT PRIMARY KEY
);

CREATE TABLE vehicles (
    vehicle_type TEXT PRIMARY KEY
);

CREATE TABLE delivery_zones (
    delivery_zone TEXT PRIMARY KEY
);

CREATE INDEX idx_deliveries_route_id ON deliveries(route_id);
CREATE INDEX idx_deliveries_driver_id ON deliveries(driver_id);
CREATE INDEX idx_deliveries_warehouse_id ON deliveries(warehouse_id);
CREATE INDEX idx_deliveries_vehicle_type ON deliveries(vehicle_type);
CREATE INDEX idx_deliveries_zone ON deliveries(delivery_zone);
CREATE INDEX idx_deliveries_sched_date ON deliveries(scheduled_delivery_date);
