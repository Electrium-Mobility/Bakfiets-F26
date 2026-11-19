/**************************************************************************
  Bakfiets F26 display (issue #22)
  Based on firmware/desk-demo. Adds: read speed and battery voltage from the
  VESC over CAN (TWAI) and show them on the screen. The ESP32 only reads.
  Board: ESP32-S3 (Tools > Board > ESP32S3 Dev Module). See firmware/README.md.

  Screen version: ILI9341 colour TFT, 320 x 240, SPI.
  Libraries: Adafruit GFX Library, Adafruit ILI9341, FastLED
 **************************************************************************/
/**************************************************************************
  Electrium Mobility Bakfiets display
  Contributers: Patrick He, Kimberley Hoang, Alisa Wu, Saptarshi Bhattacherya
 **************************************************************************/
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
#include <FastLED.h>
#include "driver/twai.h"

// ---------------- Screen (ILI9341, SPI) ----------------
// Screen pin -> ESP32-S3 GPIO
#define TFT_CLK   12   // SCK
#define TFT_MOSI  11   // MOSI (data from ESP32 to screen)
#define TFT_CS    10   // CS   (chip select)
#define TFT_DC     9   // D/C  (data / command)
#define TFT_RST    8   // RST  (reset)
// LED (backlight) -> 3.3V,  VCC -> 3.3V,  GND -> GND,  MISO not used

Adafruit_ILI9341 tft(TFT_CS, TFT_DC, TFT_RST);   // uses the hardware SPI bus

#define TEXT_COLOR  ILI9341_WHITE
#define BG_COLOR    ILI9341_BLACK

#define LED_PIN     5   
#define NUM_LEDS    125

CRGB leds[NUM_LEDS];

// ---------------- CAN (TWAI) ----------------
#define CAN_TX_PIN 17
#define CAN_RX_PIN 18

// VESC status message types (message.identifier >> 8)
#define VESC_STATUS_1 9    // ERPM in bytes 0-3
#define VESC_STATUS_5 27   // battery voltage x10 in bytes 4-5

#define VESC_TIMEOUT_MS   1000  // show "no VESC" after this long with no message
#define SCREEN_PERIOD_MS  100   // check whether the screen needs updating this often

// ---------------- Conversion constants ----------------
// PLACEHOLDERS until we measure ours (issue #22, step 8)
#define POLE_PAIRS             23
#define WHEEL_CIRCUMFERENCE_M  1.9f

#define BATTERY_EMPTY_V  37.0f   // 0 %
#define BATTERY_FULL_V   50.4f   // 100 %

// ---------------- Latest data from the VESC ----------------
bool canStarted = false;
bool haveErpm = false;
bool haveVolts = false;
int32_t latestErpm = 0;
float latestVolts = 0.0f;
unsigned long lastMessageMs = 0;
unsigned long lastScreenMs = 0;

// -1 = not drawn yet
int shownMode = -1;
int shownBattery = -1;
int shownSpeed = -1;     

void setupCan() {
  // NORMAL mode

  twai_general_config_t g_config = TWAI_GENERAL_CONFIG_DEFAULT((gpio_num_t)CAN_TX_PIN, (gpio_num_t)CAN_RX_PIN, TWAI_MODE_NORMAL);
  twai_timing_config_t t_config = TWAI_TIMING_CONFIG_500KBITS();
  twai_filter_config_t f_config = TWAI_FILTER_CONFIG_ACCEPT_ALL();

  if (twai_driver_install(&g_config, &t_config, &f_config) != ESP_OK) {
    Serial.println(F("TWAI: failed to install driver"));
    return;
  }
  if (twai_start() != ESP_OK) {
    Serial.println(F("TWAI: failed to start driver"));
    return;
  }
  Serial.println(F("TWAI: started"));
  canStarted = true;
}


void readCan() {
  if (!canStarted) {
    return;
  }

  twai_message_t message;
  while (twai_receive(&message, 0) == ESP_OK) {
    if (!message.extd || message.rtr) {
      continue;  // Extended data frames
    }

    uint32_t type = message.identifier >> 8;

    if (type == VESC_STATUS_1 && message.data_length_code >= 4) {
      latestErpm = (int32_t)(((uint32_t)message.data[0] << 24) |
                             ((uint32_t)message.data[1] << 16) |
                             ((uint32_t)message.data[2] << 8) |
                             (uint32_t)message.data[3]);
      haveErpm = true;
      lastMessageMs = millis();
    } else if (type == VESC_STATUS_5 && message.data_length_code >= 6) {
      int16_t raw = (int16_t)(((uint16_t)message.data[4] << 8) | message.data[5]);
      latestVolts = raw / 10.0f;
      haveVolts = true;
      lastMessageMs = millis();
    }
  }
}

bool vescConnected() {
  if (!haveErpm && !haveVolts) {
    return false;
  }
  return (millis() - lastMessageMs) < VESC_TIMEOUT_MS;
}

// Speed in km/h = ERPM / pole pairs x wheel circumference (m) x 60 / 1000
uint8_t speedKmh() {
  float erpm = latestErpm;
  if (erpm < 0) {
    erpm = -erpm;
  }
  float kmh = erpm / POLE_PAIRS * WHEEL_CIRCUMFERENCE_M * 60.0f / 1000.0f;
  if (kmh > 255.0f) {
    kmh = 255.0f;
  }
  return (uint8_t)(kmh + 0.5f);
}

// Battery %: a straight line from BATTERY_EMPTY_V (0 %) to BATTERY_FULL_V (100 %)
uint8_t batteryPercent() {
  float percent = (latestVolts - BATTERY_EMPTY_V) / (BATTERY_FULL_V - BATTERY_EMPTY_V) * 100.0f;
  if (percent < 0.0f) {
    percent = 0.0f;
  }
  if (percent > 100.0f) {
    percent = 100.0f;
  }
  return (uint8_t)(percent + 0.5f);
}

void setup() {
  Serial.begin(9600);

  // Start the SPI bus on our chosen pins (SCK, MISO, MOSI, SS).
  SPI.begin(TFT_CLK, -1, TFT_MOSI, TFT_CS);

  tft.begin();
  tft.setRotation(1);          // landscape: 320 wide, 240 tall
  tft.fillScreen(BG_COLOR);
  Serial.println(F("ILI9341: started"));

  FastLED.addLeds<WS2813, LED_PIN, GRB>(leds, NUM_LEDS); // Initialize FastLED
  FastLED.setBrightness(50); // Set the brightness of the LEDs (0-255)

  // Clear all LEDs to off initially
  FastLED.clear();
  FastLED.show();

  setupCan();
}



// Battery icon + percentage, top left
void drawBattery(uint8_t percentage) {
  int16_t batteryWidth = 118;
  int16_t batteryHeight = 48;
  int16_t batteryX = 10;
  int16_t batteryY = 20;

  int16_t innerWidth = batteryWidth - 8;
  int16_t fillWidth = innerWidth * percentage / 100;

  // battery 
  tft.drawRect(batteryX, batteryY, batteryWidth, batteryHeight, TEXT_COLOR);
  tft.fillRect(batteryX + batteryWidth, batteryY + 14, 6, batteryHeight - 28, TEXT_COLOR);

  tft.fillRect(batteryX + 4, batteryY + 4, fillWidth, batteryHeight - 8, TEXT_COLOR);
  tft.fillRect(batteryX + 4 + fillWidth, batteryY + 4, innerWidth - fillWidth, batteryHeight - 8, BG_COLOR);

  // percentage
  char text[6];
  snprintf(text, sizeof(text), "%3u%%", percentage);
  tft.setTextSize(3, 6);                    
  tft.setTextColor(TEXT_COLOR, BG_COLOR);   
  tft.setCursor(145, 20);
  tft.print(text);
}

// Speed in KM/H, bottom left
void drawSpeed(uint8_t speed) {
  if (speed > 99) {
    speed = 99;   
  }

  char text[4];
  snprintf(text, sizeof(text), "%2u", speed);
  tft.setTextSize(7, 15);                   
  tft.setTextColor(TEXT_COLOR, BG_COLOR);
  tft.setCursor(24, 108);
  tft.print(text);

  tft.setTextSize(2, 5);                    
  tft.setCursor(134, 130);
  tft.print(F("KM"));
  tft.setCursor(170, 165);
  tft.print(F("H"));
  tft.drawLine(175, 150, 152, 185, TEXT_COLOR);
  tft.drawLine(176, 150, 153, 185, TEXT_COLOR);  
}

// Power Assist (PA) level
void drawLevel(uint8_t level) {
  tft.setTextSize(4, 6);                    
  tft.setTextColor(TEXT_COLOR, BG_COLOR);
  tft.setCursor(258, 20);
  tft.print(F("PA"));

  tft.setTextSize(4, 12);                   
  tft.setCursor(270, 120);
  tft.print(level);
}

// Shown when no CAN message has arrived for VESC_TIMEOUT_MS
void drawNoVesc() {
  tft.setTextSize(4);
  tft.setTextColor(TEXT_COLOR, BG_COLOR);
  tft.setCursor(20, 100);
  tft.print(F("no VESC"));
}

// LED animation for left turn
void leftTurn() {
  for (int i = NUM_LEDS/2; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Red; FastLED.show(); delay(10);
  }

  for (int i = NUM_LEDS/2; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black; FastLED.show(); delay(10);
  }
}

// LED animation for right turn
void rightTurn() {
  for (int i = NUM_LEDS/2; i >= 0; i--) {
    leds[i] = CRGB::Red; FastLED.show(); delay(10);
  }
  for (int i = NUM_LEDS/2; i >= 0; i--) {
    leds[i] = CRGB::Black; FastLED.show(); delay(10);
  }
}


void drawScreen() {
  int mode = vescConnected() ? 1 : 0;

  // Mode changed ("no VESC" <-> connected): wipe the screen and draw the fixed parts
  if (mode != shownMode) {
    tft.fillScreen(BG_COLOR);

    // Screen divider
    tft.drawFastVLine(232, 10, 220, TEXT_COLOR);

    // PA Level
    uint8_t level = 5; // hard coded
    drawLevel(level);

    if (mode == 0) {
      drawNoVesc();
    }

    shownMode = mode;
    shownBattery = -1;   // force battery and speed to be drawn again
    shownSpeed = -1;
  }

  if (mode == 1) {
    // Battery display
    if (haveVolts) {
      int percent = batteryPercent();
      if (percent != shownBattery) {
        drawBattery(percent);
        shownBattery = percent;
      }
    }

    // Speed
    if (haveErpm) {
      int speed = speedKmh();
      if (speed != shownSpeed) {
        drawSpeed(speed);
        shownSpeed = speed;
      }
    }
  }
}

void loop() {
  // 1. Empty the CAN receive queue 
  readCan();

  // 2. Check the screen every SCREEN_PERIOD_MS
  unsigned long now = millis();
  if (now - lastScreenMs >= SCREEN_PERIOD_MS) {
    lastScreenMs = now;
    drawScreen();
  }
}
