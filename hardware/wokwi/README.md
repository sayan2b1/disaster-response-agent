# Wokwi ESP32 Edge Siren Beacon Simulation Guide

This folder contains the complete firmware and circuit definition to simulate the **Regional Disaster Response Agent's IoT Field Beacon** on [Wokwi.com](https://wokwi.com).

## 1. What This Hardware Simulation Represents
In real-world disaster management (e.g., Sundarbans cyclones, North Bengal hill landslides, Gangetic flooding), cellular towers and civilian smartphones frequently lose power or experience cell network congestion.

This **ESP32 Edge Beacon** acts as a decentralized municipal warning hub stationed at:
- Flood relief centers and cyclone shelters
- River embankment sluice gates & bridges
- Coastal police checkpoints and panchayat offices

The central AI Disaster Response Agent transmits emergency evacuation directives, which the ESP32 receives, rendering them on an outdoor **16x2 I2C LCD**, flashing **high-intensity siren LEDs**, and sounding an audible **piezo siren alarm**.

---

## 2. Quick Setup in Wokwi (Under 60 Seconds)

1. Open your Wokwi project or navigate to [wokwi.com/projects/new/esp32](https://wokwi.com/projects/new/esp32).
2. Open the **`sketch.ino`** tab, delete anything inside, and paste the code from [`sketch.ino`](./sketch.ino).
3. Open the **`diagram.json`** tab, delete anything inside, and paste the code from [`diagram.json`](./diagram.json).
4. Open the **`libraries.txt`** tab and make sure `LiquidCrystal I2C` is listed.
5. Click the green **Play (▶️)** button to start the simulation!

---

## 3. How to Interact with the Hardware in Wokwi

### A. Live Serial Monitor Commands
In the Wokwi Serial Monitor window at the bottom of the screen, you can type commands as if you were the central AI Agent:
- `ALERT:KOLKATA:CRITICAL:ROUTE 1 CLEAR` $\rightarrow$ Instantly switches to Kolkata, turns on Red Siren LED, pulses buzzer, and displays Route 1 Clear.
- `ALERT:DIGHA:CRITICAL:INLAND HIGHWAY` $\rightarrow$ Coastal surge protocol.
- `ALERT:KALYANI:LOW:ALL ROADS OPEN` $\rightarrow$ Turns Green LED on, silences buzzer, normal monitoring.
- `CRITICAL` / `MODERATE` / `LOW` $\rightarrow$ Quick threat level override.

### B. Physical Pushbutton (Local Override)
- Click the blue push button wired to GPIO 32.
- Each click advances the beacon through preset disaster scenarios (Tamluk, Digha, Kolkata, Darjeeling, Kalyani).

### C. Automatic Dual-Screen Display Rotation
The 16x2 LCD screen automatically rotates every 3.2 seconds between:
- **Screen 1**: Target Municipality, Threat Severity tag (`[CRIT!]`, `[WATCH]`), and Primary Evacuation Corridor.
- **Screen 2**: Live Meteorological Telemetry (Rainfall mm, Wind Speed km/h) and Logistics Allocation (Boats, Sandbags).

---

## 4. Hardware Pinout Table

| Peripheral | ESP32 Pin | Function |
| :--- | :--- | :--- |
| **I2C LCD SDA** | `GPIO 21` | Serial Data |
| **I2C LCD SCL** | `GPIO 22` | Serial Clock |
| **I2C LCD VCC** | `VIN (5V)` | Display Power |
| **I2C LCD GND** | `GND` | Ground |
| **Red Siren LED** | `GPIO 18` | Critical Alarm Beacon (Pulsing Strobe) |
| **Yellow LED** | `GPIO 19` | Moderate Advisory Watch Indicator |
| **Green LED** | `GPIO 23` | Low Hazard Normal Operation Indicator |
| **Piezo Buzzer** | `GPIO 25` | Audible Tactical Alert Siren (1200 Hz) |
| **Push Button** | `GPIO 32` | Local Scenario Cycle / Field Override |
