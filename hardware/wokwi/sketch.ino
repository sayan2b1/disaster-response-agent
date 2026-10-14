/*
 * Regional Disaster Response Agent - ESP32 Edge Siren Beacon
 * Wokwi Hardware Simulation (sketch.ino)
 * 
 * Target Board: ESP32 DevKit v1
 * Display: 16x2 I2C LCD (PCF8574 at 0x27)
 * Pinout:
 *   - I2C SDA -> GPIO 21
 *   - I2C SCL -> GPIO 22
 *   - Red Alert LED -> GPIO 18
 *   - Yellow Watch LED -> GPIO 19
 *   - Green Normal LED -> GPIO 23
 *   - Piezo Siren Buzzer -> GPIO 25
 *   - Local Override Button -> GPIO 32 (Internal Pullup)
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Hardware Pin Definitions
const int PIN_LED_RED    = 18;
const int PIN_LED_YELLOW = 19;
const int PIN_LED_GREEN  = 23;
const int PIN_BUZZER     = 25;
const int PIN_BUTTON     = 32;

// Telemetry Alert Packet Structure
struct AlertDirective {
  String region;
  String threatLevel; // "CRITICAL", "MODERATE", "LOW"
  String evacRoute;
  float precipMm;
  float windKmh;
  int boats;
  int sandbags;
};

// Default Initial Directive matching Tamluk Coastal Baseline
AlertDirective currentAlert = {
  "TAMLUK",
  "CRITICAL",
  "ROUTE 1 CLEAR",
  24.5,
  48.0,
  25,
  5000
};

// Preset Scenarios for Local Field Demonstration (Toggle via Button)
const AlertDirective PRESETS[] = {
  {"TAMLUK",     "CRITICAL", "ROUTE 1 CLEAR",   24.5, 48.0, 25, 5000},
  {"DIGHA",      "CRITICAL", "INLAND ELEVATED", 28.5, 65.0, 35, 6500},
  {"KOLKATA",    "MODERATE", "BYPASS FLYOVER",  10.5, 32.0, 10, 2000},
  {"DARJEELING", "CRITICAL", "RIDGE CORRIDOR",  32.0, 42.0,  5, 4000},
  {"KALYANI",    "LOW",      "ALL ROADS OPEN",   1.5, 14.0,  2,  500}
};
const int TOTAL_PRESETS = sizeof(PRESETS) / sizeof(PRESETS[0]);
int currentPresetIdx = 0;

// Timing & Display Rotation
unsigned long lastScreenFlip = 0;
bool showingScreenA = true;
unsigned long lastStrobe = 0;
bool strobeState = false;

void setup() {
  Serial.begin(115200);
  delay(100);

  // Initialize GPIO
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_LED_YELLOW, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_BUTTON, INPUT_PULLUP);

  // Initialize LCD Screen
  lcd.init();
  lcd.backlight();

  // Boot Sequence Splash
  lcd.setCursor(0, 0);
  lcd.print("DISASTER AGENT");
  lcd.setCursor(0, 1);
  lcd.print("EDGE BEACON v1.0");
  
  // Quick self-test LEDs & Buzzer chirp
  digitalWrite(PIN_LED_GREEN, HIGH);
  delay(200);
  digitalWrite(PIN_LED_YELLOW, HIGH);
  delay(200);
  digitalWrite(PIN_LED_RED, HIGH);
  tone(PIN_BUZZER, 1760, 120);
  delay(800);

  // Clear splash and apply default alert
  applyAlertOutputs();

  Serial.println("\n========================================================");
  Serial.println("   REGIONAL DISASTER RESPONSE AGENT - EDGE IOT BEACON   ");
  Serial.println("   Connected to ESP32 DevKit v1 | I2C LCD @ 0x27        ");
  Serial.println("========================================================");
  Serial.println("Type commands in this Serial Monitor to update the beacon:");
  Serial.println("  1. ALERT:KOLKATA:CRITICAL:ROUTE 1 CLEAR");
  Serial.println("  2. ALERT:DIGHA:CRITICAL:INLAND ELEVATED");
  Serial.println("  3. CRITICAL / MODERATE / LOW");
  Serial.println("Or press the button on GPIO 32 to cycle cities locally.");
  Serial.println("========================================================\n");
}

void loop() {
  // 1. Process incoming Serial commands from Central AI Agent
  if (Serial.available() > 0) {
    String inputLine = Serial.readStringUntil('\n');
    inputLine.trim();
    if (inputLine.length() > 0) {
      handleSerialDirective(inputLine);
    }
  }

  // 2. Hardware Button Handler (cycles cities on local beacon)
  if (digitalRead(PIN_BUTTON) == LOW) {
    delay(250); // Debounce
    currentPresetIdx = (currentPresetIdx + 1) % TOTAL_PRESETS;
    currentAlert = PRESETS[currentPresetIdx];
    applyAlertOutputs();
    Serial.println("[BEACON-LOCAL] Manual override button pressed. Ingested: " + currentAlert.region);
  }

  // 3. Alternate between Screen 1 (Evacuation Route) and Screen 2 (Weather & Logistics)
  if (millis() - lastScreenFlip > 3200) {
    lastScreenFlip = millis();
    showingScreenA = !showingScreenA;
    renderLcdDisplay();
  }

  // 4. Critical Alarm Siren Strobing
  if (currentAlert.threatLevel == "CRITICAL") {
    if (millis() - lastStrobe > 350) {
      lastStrobe = millis();
      strobeState = !strobeState;
      digitalWrite(PIN_LED_RED, strobeState ? HIGH : LOW);
      if (strobeState) {
        tone(PIN_BUZZER, 1200, 120); // Tactical alert pulse
      } else {
        noTone(PIN_BUZZER);
      }
    }
  }
}

void applyAlertOutputs() {
  // Reset all outputs
  digitalWrite(PIN_LED_RED, LOW);
  digitalWrite(PIN_LED_YELLOW, LOW);
  digitalWrite(PIN_LED_GREEN, LOW);
  noTone(PIN_BUZZER);

  if (currentAlert.threatLevel == "CRITICAL") {
    digitalWrite(PIN_LED_RED, HIGH);
    tone(PIN_BUZZER, 1800, 300); // Startup chirp
  } else if (currentAlert.threatLevel == "MODERATE") {
    digitalWrite(PIN_LED_YELLOW, HIGH);
    tone(PIN_BUZZER, 880, 100);
  } else {
    digitalWrite(PIN_LED_GREEN, HIGH);
  }

  renderLcdDisplay();
}

void renderLcdDisplay() {
  lcd.clear();

  if (showingScreenA) {
    // Screen A: Target Region & Evacuation Corridor Directive
    lcd.setCursor(0, 0);
    String header = currentAlert.region;
    if (currentAlert.threatLevel == "CRITICAL") header += " [CRIT!]";
    else if (currentAlert.threatLevel == "MODERATE") header += " [WATCH]";
    else header += " [NORMAL]";
    lcd.print(header.substring(0, 16));

    lcd.setCursor(0, 1);
    String routeLine = "EVAC:" + currentAlert.evacRoute;
    lcd.print(routeLine.substring(0, 16));
  } else {
    // Screen B: Live Meteorological Telemetry & Allocated Logistics
    lcd.setCursor(0, 0);
    char line1[17];
    snprintf(line1, sizeof(line1), "R:%.1fmm W:%.0fk", currentAlert.precipMm, currentAlert.windKmh);
    lcd.print(line1);

    lcd.setCursor(0, 1);
    char line2[17];
    snprintf(line2, sizeof(line2), "BT:%d SAND:%d", currentAlert.boats, currentAlert.sandbags);
    lcd.print(line2);
  }
}

void handleSerialDirective(String cmd) {
  cmd.toUpperCase();
  
  if (cmd.startsWith("ALERT:")) {
    // Format: ALERT:REGION:THREAT:ROUTE
    // Example: ALERT:KOLKATA:CRITICAL:ROUTE 1 CLEAR
    int p1 = cmd.indexOf(':', 6);
    int p2 = cmd.indexOf(':', p1 + 1);

    if (p1 != -1) {
      currentAlert.region = cmd.substring(6, p1);
      if (p2 != -1) {
        currentAlert.threatLevel = cmd.substring(p1 + 1, p2);
        currentAlert.evacRoute = cmd.substring(p2 + 1);
      } else {
        currentAlert.threatLevel = cmd.substring(p1 + 1);
        currentAlert.evacRoute = "ROUTE CLEAR";
      }
      applyAlertOutputs();
      Serial.println("[AI-DIRECTIVE-RECEIVED] Updated " + currentAlert.region + " -> " + currentAlert.threatLevel);
    }
  } else if (cmd == "CRITICAL" || cmd == "MODERATE" || cmd == "LOW") {
    currentAlert.threatLevel = cmd;
    applyAlertOutputs();
    Serial.println("[THREAT-LEVEL-OVERRIDE] Set to " + cmd);
  } else if (cmd == "HELP") {
    Serial.println("Send formatted command: ALERT:<REGION>:<THREAT>:<ROUTE>");
    Serial.println("Example: ALERT:DIGHA:CRITICAL:INLAND HIGHWAY");
  } else {
    Serial.println("[RX-UNKNOWN] Try sending: ALERT:HALDIA:CRITICAL:BYPASS OPEN");
  }
}
