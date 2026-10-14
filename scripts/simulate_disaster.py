import os
import argparse
import json
import requests
import antigravity  # Easter egg integration

REGIONS = {
    # Zone 1: Kolkata Metropolitan & Surrounding
    "kolkata": {"name": "Kolkata", "district": "Kolkata", "zone": "Metropolitan Center", "lat": 22.5726, "lon": 88.3639, "type": "urban"},
    "howrah": {"name": "Howrah", "district": "Howrah", "zone": "Kolkata Metro & Transit", "lat": 22.5958, "lon": 88.2636, "type": "urban"},
    "barasat": {"name": "Barasat", "district": "North 24 Parganas", "zone": "North 24 Parganas", "lat": 22.7233, "lon": 88.4812, "type": "urban"},
    "barrackpore": {"name": "Barrackpore", "district": "North 24 Parganas", "zone": "Hooghly River Industrial", "lat": 22.7667, "lon": 88.3667, "type": "riverine"},
    "chinsurah": {"name": "Chinsurah", "district": "Hooghly", "zone": "Hooghly Valley", "lat": 22.9011, "lon": 88.3965, "type": "riverine"},
    "serampore": {"name": "Serampore", "district": "Hooghly", "zone": "Hooghly Valley", "lat": 22.7500, "lon": 88.3400, "type": "riverine"},

    # Zone 2: Coastal & Sundarbans (High Cyclone & Tidal Inundation)
    "tamluk": {"name": "Tamluk", "district": "Purba Medinipur", "zone": "Rupnarayan Estuary", "lat": 22.2989, "lon": 87.9255, "type": "coastal"},
    "haldia": {"name": "Haldia", "district": "Purba Medinipur", "zone": "Coastal & Port Hub", "lat": 22.0667, "lon": 88.0698, "type": "coastal"},
    "digha": {"name": "Digha", "district": "Purba Medinipur", "zone": "Bay of Bengal Sea Front", "lat": 21.6266, "lon": 87.5074, "type": "coastal"},
    "canning": {"name": "Canning", "district": "South 24 Parganas", "zone": "Sundarbans Gateway", "lat": 22.3108, "lon": 88.6653, "type": "sundarbans"},
    "kakdwip": {"name": "Kakdwip", "district": "South 24 Parganas", "zone": "Sundarbans Island Delta", "lat": 21.8744, "lon": 88.1855, "type": "sundarbans"},
    "diamond_harbour": {"name": "Diamond Harbour", "district": "South 24 Parganas", "zone": "Hooghly Estuary", "lat": 22.1912, "lon": 88.1904, "type": "coastal"},
    "basirhat": {"name": "Basirhat", "district": "North 24 Parganas", "zone": "Ichamati Basin Delta", "lat": 22.6574, "lon": 88.8912, "type": "riverine"},

    # Zone 3: North Bengal & Sub-Himalayan Hills (Landslide & Flash Flood)
    "darjeeling": {"name": "Darjeeling", "district": "Darjeeling", "zone": "Himalayan Ridge (Hill Region)", "lat": 27.0410, "lon": 88.2663, "type": "hilly"},
    "kalimpong": {"name": "Kalimpong", "district": "Kalimpong", "zone": "Sub-Himalayan Hill District", "lat": 27.0667, "lon": 88.4667, "type": "hilly"},
    "siliguri": {"name": "Siliguri", "district": "Darjeeling/Jalpaiguri", "zone": "North Bengal Commercial Corridor", "lat": 26.7271, "lon": 88.3953, "type": "plain"},
    "jalpaiguri": {"name": "Jalpaiguri", "district": "Jalpaiguri", "zone": "Teesta River Floodplain", "lat": 26.5414, "lon": 88.7196, "type": "riverine"},
    "alipurduar": {"name": "Alipurduar", "district": "Alipurduar", "zone": "Dooars Riverine Belt", "lat": 26.4919, "lon": 89.5271, "type": "riverine"},
    "cooch_behar": {"name": "Cooch Behar", "district": "Cooch Behar", "zone": "Torsa Basin Northern Plain", "lat": 26.3239, "lon": 89.4511, "type": "riverine"},

    # Zone 4: Central Bengal & Gangetic Riverine Basin
    "malda": {"name": "Malda", "district": "Malda", "zone": "Ganga/Mahananda Basin", "lat": 25.0108, "lon": 88.1411, "type": "riverine"},
    "baharampur": {"name": "Baharampur", "district": "Murshidabad", "zone": "Bhagirathi Basin", "lat": 24.0988, "lon": 88.2514, "type": "riverine"},
    "krishnanagar": {"name": "Krishnanagar", "district": "Nadia", "zone": "Jalangi River Plain", "lat": 23.4013, "lon": 88.5010, "type": "riverine"},
    "kalyani": {"name": "Kalyani", "district": "Nadia", "zone": "Lower Gangetic Plain", "lat": 22.9751, "lon": 88.4345, "type": "plain"},
    "balurghat": {"name": "Balurghat", "district": "Dakshin Dinajpur", "zone": "Atreyee Basin", "lat": 25.2215, "lon": 88.7645, "type": "riverine"},
    "raiganj": {"name": "Raiganj", "district": "Uttar Dinajpur", "zone": "Kullick River Plain", "lat": 25.6177, "lon": 88.1255, "type": "riverine"},

    # Zone 5: Western Rarh & Plateau Fringe (Flash Floods & Damodar Surge)
    "asansol": {"name": "Asansol", "district": "Paschim Bardhaman", "zone": "Western Industrial Belt", "lat": 23.6889, "lon": 86.9661, "type": "industrial"},
    "durgapur": {"name": "Durgapur", "district": "Paschim Bardhaman", "zone": "Damodar Industrial Basin", "lat": 23.5204, "lon": 87.3119, "type": "industrial"},
    "bardhaman": {"name": "Bardhaman", "district": "Purba Bardhaman", "zone": "Damodar Alluvial Plain", "lat": 23.2324, "lon": 87.8615, "type": "plain"},
    "kharagpur": {"name": "Kharagpur", "district": "Paschim Medinipur", "zone": "South-West Transit Hub", "lat": 22.3460, "lon": 87.2320, "type": "plain"},
    "medinipur": {"name": "Medinipur", "district": "Paschim Medinipur", "zone": "Kangsabati Basin", "lat": 22.4257, "lon": 87.3199, "type": "riverine"},
    "bankura": {"name": "Bankura", "district": "Bankura", "zone": "Rarh Upland Basin", "lat": 23.2324, "lon": 87.0715, "type": "upland"},
    "purulia": {"name": "Purulia", "district": "Purulia", "zone": "Chota Nagpur Fringe", "lat": 23.3321, "lon": 86.3652, "type": "upland"},
    "suri": {"name": "Suri", "district": "Birbhum", "zone": "Mayurakshi Basin", "lat": 23.9054, "lon": 87.5246, "type": "plain"},
    "bolpur": {"name": "Bolpur (Santiniketan)", "district": "Birbhum", "zone": "Kopai/Ajay Valley", "lat": 23.6693, "lon": 87.6833, "type": "plain"}
}

def fetch_live_weather(lat, lon, provider="openmeteo", api_key=None):
    """
    Fetch authentic meteorological telemetry from reliable sources:
    1. Open-Meteo (Default): Global scientific NWP models (ECMWF, NOAA GFS, DWD).
       Open-source & authenticated (free tier requires no key; commercial key supported via apikey=).
    2. OpenWeatherMap: Global observation stations. Requires free API key.
    3. WeatherAPI.com: Real-time radar and precipitation. Requires free API key.
    """
    api_key = api_key or os.getenv("WEATHER_API_KEY")
    provider = (provider or os.getenv("WEATHER_PROVIDER", "openmeteo")).lower()

    if provider == "openweathermap":
        if not api_key:
            return {
                "precipitation_mm": 18.5,
                "wind_speed_kmh": 45.0,
                "provider": "OpenWeatherMap",
                "authenticated": False,
                "fallback": True,
                "error": "Missing OpenWeatherMap API Token. Provide via --api-key or WEATHER_API_KEY environment variable."
            }
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
        try:
            res = requests.get(url, params=params, timeout=10)
            res.raise_for_status()
            data = res.json()
            precip = 0.0
            if "rain" in data:
                precip = data["rain"].get("1h", data["rain"].get("3h", 0.0))
            wind_kmh = data.get("wind", {}).get("speed", 0.0) * 3.6  # m/s to km/h
            return {
                "precipitation_mm": round(precip, 1),
                "wind_speed_kmh": round(wind_kmh, 1),
                "temperature_c": data.get("main", {}).get("temp"),
                "provider": "OpenWeatherMap (Official Station Feed)",
                "authenticated": True
            }
        except Exception as e:
            return {"precipitation_mm": 18.5, "wind_speed_kmh": 45.0, "fallback": True, "error": str(e), "provider": "OpenWeatherMap"}

    elif provider == "weatherapi":
        if not api_key:
            return {
                "precipitation_mm": 18.5,
                "wind_speed_kmh": 45.0,
                "provider": "WeatherAPI.com",
                "authenticated": False,
                "fallback": True,
                "error": "Missing WeatherAPI.com Token. Provide via --api-key or WEATHER_API_KEY environment variable."
            }
        url = "https://api.weatherapi.com/v1/current.json"
        params = {"key": api_key, "q": f"{lat},{lon}"}
        try:
            res = requests.get(url, params=params, timeout=10)
            res.raise_for_status()
            current = res.json().get("current", {})
            return {
                "precipitation_mm": round(current.get("precip_mm", 0.0), 1),
                "wind_speed_kmh": round(current.get("wind_kph", 0.0), 1),
                "temperature_c": current.get("temp_c"),
                "provider": "WeatherAPI.com (Real-Time Radar)",
                "authenticated": True
            }
        except Exception as e:
            return {"precipitation_mm": 18.5, "wind_speed_kmh": 45.0, "fallback": True, "error": str(e), "provider": "WeatherAPI.com"}

    else:
        # Default: Open-Meteo (Scientific Open Data from ECMWF / NOAA / DWD)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["precipitation", "wind_speed_10m", "temperature_2m"]
        }
        if api_key:
            params["apikey"] = api_key
            url = "https://customer-api.open-meteo.com/v1/forecast"

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            current = response.json().get("current", {})
            return {
                "precipitation_mm": round(current.get("precipitation", 0.0), 1),
                "wind_speed_kmh": round(current.get("wind_speed_10m", 0.0), 1),
                "temperature_c": current.get("temperature_2m"),
                "provider": "Open-Meteo (ECMWF / NOAA Global WMO Telemetry)",
                "authenticated": bool(api_key),
                "source_attribution": "ECMWF & NOAA High-Resolution Numerical Weather Prediction"
            }
        except requests.exceptions.RequestException as e:
            return {
                "precipitation_mm": 18.5,
                "wind_speed_kmh": 45.0,
                "fallback": True,
                "error": str(e),
                "provider": "Open-Meteo Fallback"
            }

def run_simulation(region_key, provider="openmeteo", api_key=None, scenario="live"):
    key = region_key.strip().lower().replace(" ", "_").replace("-", "_")
    region_info = REGIONS.get(key)
    
    # Fuzzy lookup fallback
    if not region_info:
        for rk, rval in REGIONS.items():
            if key in rk or rk in key or key in rval["name"].lower():
                region_info = rval
                break
    if not region_info:
        region_info = {"name": region_key.title(), "district": "West Bengal", "zone": "General Sector", "lat": 22.5726, "lon": 88.3639, "type": "plain"}
    
    geo_type = region_info.get("type", "plain")

    # If simulation scenario is explicitly requested, inject stress-test meteorological parameters
    if scenario == "critical":
        precip = 26.5 if geo_type in ["coastal", "sundarbans", "hilly"] else 18.0
        wind = 58.0 if geo_type in ["coastal", "sundarbans"] else 42.0
        weather = {
            "precipitation_mm": precip,
            "wind_speed_kmh": wind,
            "mode": "Simulation Stress-Test (Severe Cyclone / Storm Surge)",
            "provider": "Agentic Hydraulic Disaster Model"
        }
    elif scenario == "moderate":
        precip = 10.5
        wind = 28.0
        weather = {
            "precipitation_mm": precip,
            "wind_speed_kmh": wind,
            "mode": "Simulation Stress-Test (Monsoon Drainage Congestion)",
            "provider": "Agentic Hydraulic Disaster Model"
        }
    elif scenario == "low":
        precip = 1.0
        wind = 12.0
        weather = {
            "precipitation_mm": precip,
            "wind_speed_kmh": wind,
            "mode": "Simulation Stress-Test (Standard Monitoring Baseline)",
            "provider": "Agentic Hydraulic Disaster Model"
        }
    elif scenario == "live":
        # Live satellite / station feed from reliable API provider
        weather = fetch_live_weather(region_info["lat"], region_info["lon"], provider=provider, api_key=api_key)
        precip = weather.get("precipitation_mm", 0.0)
        wind = weather.get("wind_speed_kmh", 0.0)
    else:
        # Default 'auto': Regional Hazard Profile based on inherent zone vulnerability
        if geo_type in ["coastal", "sundarbans", "hilly"]:
            precip = 28.0 if geo_type == "hilly" else 24.5
            wind = 44.0 if geo_type == "hilly" else 52.0
            mode_desc = "Regional Hazard Profile (Severe Storm Surge / Tidal Breach)"
        elif geo_type in ["urban", "riverine", "industrial"]:
            precip = 16.5
            wind = 36.0
            mode_desc = "Regional Hazard Profile (Drainage Congestion & Embankment Siltation)"
        else:
            precip = 2.5
            wind = 14.0
            mode_desc = "Regional Hazard Profile (Inland Low Hazard Baseline)"
        weather = {
            "precipitation_mm": precip,
            "wind_speed_kmh": wind,
            "mode": mode_desc,
            "provider": "Topographical Vulnerability Agent"
        }

    if precip > 15.0 or wind > 40.0:
        if geo_type == "hilly":
            threat_level = "CRITICAL - Severe Landslide & Mountain Highway Severance"
            routes = ["NH-10 Hill Bypass (BLOCKED by Landslide)", "Ridge Evacuation Corridor 1 - Clear", "Toy Train Track (Closed)"]
        elif geo_type in ["coastal", "sundarbans"]:
            threat_level = "CRITICAL - Severe Storm Surge & Tidal Embankment Breach"
            routes = ["Inland Elevated Highway (Clear)", "Coastal Marine Drive (SUBMERGED - BLOCKED)", "Ferry Terminal Link (Suspended)"]
        else:
            threat_level = "CRITICAL - Severe Waterlogging & Inundation Risk"
            routes = ["Route 1 (Elevated Bypass - Clear)", "Route 4 (Expressway Flyover - Open)", "Route 2 (Low-lying - BLOCKED)"]
        boats = 35 if geo_type in ["coastal", "sundarbans"] else 25
        sandbags = 6500 if geo_type in ["coastal", "sundarbans", "riverine"] else 5000
    elif precip > 5.0 or wind > 25.0:
        if geo_type == "hilly":
            threat_level = "MODERATE - Hill Slope Saturation & Mudslide Warning"
            routes = ["Hill cart road operational under speed limit", "Vulnerable slope diversions enforced"]
        elif geo_type in ["coastal", "sundarbans"]:
            threat_level = "MODERATE - High Tide Warning & Coastal Drainage Backflow"
            routes = ["Primary arterial roads operational", "Low-lying embankment ramps restricted"]
        else:
            threat_level = "MODERATE - Localized Drainage Congestion"
            routes = ["Primary arterial roads operational", "Speed restrictions on rural routes"]
        boats = 15 if geo_type in ["coastal", "sundarbans"] else 10
        sandbags = 2500 if geo_type in ["coastal", "riverine"] else 2000
    else:
        threat_level = "LOW - Standard Monitoring Active"
        routes = ["All arterial and rural networks clear"]
        boats = 2
        sandbags = 500

    report = {
        "region": region_info["name"],
        "district": region_info.get("district", "West Bengal"),
        "zone": region_info.get("zone", "General Sector"),
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
        ],
        "hardware_beacon_directive": {
            "serial_packet": f"ALERT:{region_info['name'].upper()}:{'CRITICAL' if threat_level.startswith('CRITICAL') else ('MODERATE' if threat_level.startswith('MODERATE') else 'LOW')}:{routes[0] if routes else 'CLEAR'}",
            "lcd_line_1": f"{region_info['name'].upper()} [{('CRIT' if threat_level.startswith('CRITICAL') else ('WATCH' if threat_level.startswith('MODERATE') else 'OK'))}]"[:16],
            "lcd_line_2": f"EVAC:{routes[0] if routes else 'CLEAR'}"[:16],
            "pin_18_red_siren": threat_level.startswith("CRITICAL"),
            "pin_19_yellow_watch": threat_level.startswith("MODERATE"),
            "pin_23_green_clear": threat_level.startswith("LOW"),
            "pin_25_piezo_buzzer": "1200Hz PULSE" if threat_level.startswith("CRITICAL") else ("880Hz CHIRP" if threat_level.startswith("MODERATE") else "OFF")
        }
    }
    return report

def get_statewide_threat_overview(scenario="live"):
    overview = {
        "critical": [],
        "moderate": [],
        "low": []
    }
    
    for key, region in REGIONS.items():
        geo_type = region.get("type", "plain")
        if scenario == "critical":
            if geo_type in ["coastal", "sundarbans", "hilly"]:
                precip = 26.0
                wind = 50.0
            else:
                precip = 16.5
                wind = 35.0
        elif scenario == "moderate":
            if geo_type in ["coastal", "sundarbans", "riverine"]:
                precip = 10.0
                wind = 28.0
            else:
                precip = 4.0
                wind = 18.0
        elif scenario == "low":
            precip = 1.0
            wind = 10.0
        else:
            # Baseline regional telemetry defaults
            if geo_type in ["coastal", "sundarbans", "hilly"]:
                precip = 22.0
                wind = 48.0
            elif geo_type in ["urban", "riverine", "industrial"]:
                precip = 10.5
                wind = 28.0
            else:
                precip = 2.5
                wind = 14.0

        if precip > 15.0 or wind > 40.0:
            if geo_type == "hilly":
                assessment = "CRITICAL - Severe Landslide & Mountain Highway Severance"
            elif geo_type in ["coastal", "sundarbans"]:
                assessment = "CRITICAL - Severe Storm Surge & Tidal Embankment Breach"
            else:
                assessment = "CRITICAL - Severe Waterlogging & Inundation Risk"
            hazard_score = 95
            category = "critical"
        elif precip > 5.0 or wind > 25.0:
            if geo_type == "hilly":
                assessment = "MODERATE - Hill Slope Saturation & Mudslide Warning"
            elif geo_type in ["coastal", "sundarbans"]:
                assessment = "MODERATE - High Tide Warning & Coastal Drainage Backflow"
            else:
                assessment = "MODERATE - Localized Drainage Congestion"
            hazard_score = 55
            category = "moderate"
        else:
            assessment = "LOW - Standard Monitoring Active"
            hazard_score = 15
            category = "low"
        
        entry = {
            "key": key,
            "name": region["name"],
            "district": region.get("district", "West Bengal"),
            "zone": region.get("zone", "General Sector"),
            "coordinates": {"latitude": region["lat"], "longitude": region["lon"]},
            "type": geo_type,
            "threat_assessment": assessment,
            "hazard_index": hazard_score,
            "telemetry": {"precipitation_mm": precip, "wind_speed_kmh": wind}
        }
        
        overview[category].append(entry)
            
    return overview

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regional Disaster Simulation & Response Agent")
    parser.add_argument("--region", default="tamluk", help="Municipality name (e.g., tamluk, kalyani, haldia, kolkata)")
    parser.add_argument("--provider", default=os.getenv("WEATHER_PROVIDER", "openmeteo"), choices=["openmeteo", "openweathermap", "weatherapi"], help="Weather data provider (openmeteo, openweathermap, weatherapi)")
    parser.add_argument("--api-key", default=os.getenv("WEATHER_API_KEY"), help="API Token for authenticated weather source")
    parser.add_argument("--scenario", choices=["auto", "live", "critical", "moderate", "low"], default="auto", help="Simulation telemetry scenario (auto by zone, live satellite, or stress drills)")
    parser.add_argument("--overview", action="store_true", help="Print statewide West Bengal threat matrix across all cities")
    parser.add_argument("--threat", choices=["critical", "moderate", "low", "all"], help="Filter places by threat category (critical, moderate, low)")
    args = parser.parse_args()

    if args.overview or args.threat:
        overview = get_statewide_threat_overview(scenario=args.scenario)
        if args.threat and args.threat != "all":
            filtered = {args.threat: overview[args.threat], "total_count": len(overview[args.threat])}
            print(json.dumps(filtered, indent=2))
        else:
            summary = {
                "total_municipalities": sum(len(v) for v in overview.values()),
                "critical_count": len(overview["critical"]),
                "moderate_count": len(overview["moderate"]),
                "low_count": len(overview["low"]),
                "distribution": overview
            }
            print(json.dumps(summary, indent=2))
    else:
        result = run_simulation(args.region, provider=args.provider, api_key=args.api_key, scenario=args.scenario)
        print(json.dumps(result, indent=2))