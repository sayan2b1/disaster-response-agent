---
name: regional-disaster-response
description: |
  Analyzes geographic, topographic, and live weather data to generate predictive disaster management protocols, evacuation paths, and emergency resource allocations for municipalities. Use this skill whenever disaster planning or regional emergency simulations are requested.
---

# Regional Disaster Simulation & Response Agent

## Purpose
Enables autonomous agents to simulate crisis scenarios, calculate hazard levels from live meteorological telemetry (via Open-Meteo), and formulate emergency management directives.

## Execution
Run the disaster simulation backend script by specifying a target municipality:

```bash
python scripts/simulate_disaster.py --region <MUNICIPALITY_NAME>
