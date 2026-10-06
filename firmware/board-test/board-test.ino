/**************************************************************************
  Bakfiets F26 board test
  Use this until we have screens. It needs nothing plugged in except USB.
  It prints the chip name once a second, so you can check two things:
    1. your laptop can upload to the board
    2. the board really is an ESP32-S3 (the desk demo needs one)

  Board: Tools > Board > esp32 > ESP32S3 Dev Module
  Set Tools > USB CDC On Boot to Enabled, then upload.
  Open Tools > Serial Monitor and set the speed (bottom right) to 115200.
 **************************************************************************/

void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.print("Hello from Bakfiets! Chip: ");
  Serial.print(ESP.getChipModel());
  Serial.print(", running for ");
  Serial.print(millis() / 1000);
  Serial.println(" s");
  delay(1000);
}
