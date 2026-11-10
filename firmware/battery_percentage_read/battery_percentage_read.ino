const int BATTERY_PIN = 1;
const float R1 = 200000.0;
const float R2 = 10000.0;
const float DIVIDER_RATIO = (R1 + R2)/R2;
const int NUM_SAMPLES = 16;
const float v_empty = 37.0;
const float v_full = 50.4;


float battery_percent(float volts){
  if (volts <= v_empty){
    return 0.0;
  }else if (volts >= v_full){
    return 100.0;
  }else{
    float batpct = (volts - v_empty)/(v_full - v_empty) * 100;
    return batpct;
  }
}


void setup() {
  Serial.begin(115200);
}

void loop() {
  long sum = 0;
  for (int i = 0; i < NUM_SAMPLES; i++){
     // Wokwi only: real hardware use analogReadMilliVolts()
    sum += analogRead(BATTERY_PIN);
  }
  int raw = sum/NUM_SAMPLES;
  int mv = raw * 3300 / 4095;
  float vbat = mv/1000.0 * DIVIDER_RATIO;
  float percent = battery_percent (vbat);

  // Used for testing data
  Serial.print("raw: ");
  Serial.print(raw);
  Serial.print("   mV: ");
  Serial.print(mv);
  Serial.print("  Vbat:  ");
  Serial.print(vbat, 2);
  
  // Actual output as a percentage
  Serial.print("   Percentage: ");
  Serial.println(percent, 0);

  delay(500);
}

