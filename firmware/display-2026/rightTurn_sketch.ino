unsigned long timeon = 0;
int i = NUM_LEDS/2;
bool color = true;

void rightTurn() {
  unsigned long interval = 10;
  unsigned long current = millis ();

  if (current - timeon >= interval){
    timeon = current;
    if (color){
      if (i >= 0){
        leds[i] = CRGB::Red;
        FastLED.show();
        i -= 1;
      }else{color = false; i = NUM_LEDS/2;}
    }else{
      if (i >= 0){
        leds[i] = CRGB::Black;
        FastLED.show();
        i -= 1;
    }else{color = true; i = NUM_LEDS/2;}
    }
  }
}