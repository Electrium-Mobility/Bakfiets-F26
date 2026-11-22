/**************************************************************************
  Bakfiets F26 LED strip test
  Plays a moving rainbow on the bay's 1 m WS2812B strip (144 LEDs).
  Wiring and photos: docs/lights/strip-desk-test.md

  Strip DIN  -> GPIO 5
  Strip 5V   -> the board's 5V pin
  Strip GND  -> the board's GND pin

  Board: Tools > Board > esp32 > ESP32S3 Dev Module (not ESP32S31)
  Port:  plug USB into the board's "USB" port, not "UART"

  Powered from USB only, so the current is capped at 400 mA in code.
  Raise the cap only once the strip runs from the 5 V power board.
 **************************************************************************/

#include <FastLED.h>

#define LED_PIN   5
#define NUM_LEDS  144

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, 400);
  FastLED.setBrightness(30);
}

void loop() {
  static uint8_t hue = 0;
  fill_rainbow(leds, NUM_LEDS, hue++, 7);
  FastLED.show();
  delay(20);
}
