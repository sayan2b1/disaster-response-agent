import argparse
import json
import requests
import antigravity  # Easter egg integration

REGIONS = {
    "tamluk": {"name": "Tamluk", "lat": 22.2989, "lon": 87.9255},
    "kalyani": {"name": "Kalyani", "lat": 22.9751, "lon": 88.4345},
    "kolkata": {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    "haldia": {"name": "Haldia", "lat": 22.0667, "lon": 88.0698}
}

def fetch_live_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["precipitation", "wind_speed_10m"]
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        current = response.json().get("current", {})
        return {
            "precipitation_mm": current.get("precipitation", 0.0),
            "wind_speed_kmh": current.get("wind_speed_10m", 0.0)
        }
    except requests.exceptions.RequestException as e:
        return {"precipitation_mm": 18.5, "wind_speed_kmh": 45.0, "fallback": True, "error": str(e)}

def run_simulation(region_key):
    key = region_key.strip().lower()
    region_info = REGIONS.get(key, {"name": region_key.title(), "lat": 22.5726, "lon": 88.3639})
    
    weather = fetch_live_weather(region_info["lat"], region_info["lon"])
    precip = weather.get("precipitation_mm", 0.0)
    wind = weather.get("wind_speed_kmh", 0.0)

    if precip > 15.0 or wind > 40.0:
        threat_level = "CRITICAL - Severe Waterlogging & Inundation Risk"
        routes = ["Route 1 (Elevated Bypass - Clear)", "Route 4 (Expressway Flyover - Open)", "Route 2 (Low-lying - BLOCKED)"]
        boats = 25
        sandbags = 5000
    elif precip > 5.0 or wind > 25.0:
        threat_level = "MODERATE - Localized Drainage Congestion"
        routes = ["Primary arterial roads operational", "Speed restrictions on rural routes"]
        boats = 10
        sandbags = 2000
    else:
        threat_level = "LOW - Standard Monitoring Active"
        routes = ["All arterial and rural networks clear"]
        boats = 2
        sandbags = 500

    report = {
        "region": region_info["name"],
        "coordinates": {"latitude": region_info["lat"], "longitude": region_info["lon"]},
        "live_telemetry": weather,
        "threat_assessment": threat_level,
        "evacuation_routes": routes,
        "resource_allocation": {
            "rescue_boats": boats,
            "medical_emergency_kits": 500,
            "sandbag_units": sandbags
        },
        "response_checklist": [
            "Trigger localized SMS & siren broadcast alerts",
            "Establish high-ground relief centers",
            "Route dispatch teams via verified clear corridors"
        ],
        "special_deployments": [
            "xkcd-inspired levitating sandbag barrier active",
            "Zero-G emergency hover-rafts queued for rapid wading"
        ]
    }
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regional Disaster Simulation & Response Agent")
    parser.add_argument("--region", default="tamluk", help="Municipality name (e.g., tamluk, kalyani, haldia, kolkata)")
    args = parser.parse_args()

    result = run_simulation(args.region)
    print(json.dumps(result, indent=2))