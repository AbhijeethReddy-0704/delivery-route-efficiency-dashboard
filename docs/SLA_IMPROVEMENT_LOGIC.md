# SLA Improvement Logic

## Objective
Estimate synthetic SLA uplift potential from targeted route optimization.

## Steps
1. Compute route-level SLA attainment (`sla_met_flag` mean by route).
2. Compute median SLA across all routes.
3. Identify bottom-performing routes (lowest ~33% by SLA).
4. For each bottom route, compute positive gap to median SLA.
5. Weight route gaps by route delivery volume.
6. Aggregate weighted uplift into a global improvement opportunity percentage.

## Interpretation
- Output is a synthetic scenario estimate, not a historical company claim.
- In this project dataset, the modeled opportunity is approximately 12%.
