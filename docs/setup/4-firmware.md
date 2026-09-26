# Setup for firmware

Finish [Setup for everyone](1-everyone.md) first.

## 1. What you need

- An **ESP32-S3 dev board**, such as the ESP32-S3-DevKitC-1. A plain ESP32 won't work: the code uses GPIO 9 and 10, which a plain ESP32 wires to its flash chip.
- An **SSD1306 128x64 I2C OLED** screen (the common 0.96-inch kind).
- Four female-to-female jumper wires and a USB-C cable.
- No LED strip is needed for the desk demo.

If you don't own these, the board and screen together cost roughly CAD $25 online.

## 2. Install Arduino IDE and ESP32 support

1. Download [Arduino IDE 2](https://www.arduino.cc/en/software) and install it.
2. Add ESP32 boards with the written guide [Installing ESP32 in Arduino IDE 2](https://randomnerdtutorials.com/installing-esp32-arduino-ide-2-0/), or watch [Set up ESP32 with Arduino IDE in 3 minutes](https://www.youtube.com/watch?v=ikBlhX-erSw).
3. Choose **Tools > Manage Libraries**, and install **Adafruit SSD1306** and **FastLED**. When asked, click **Install all**; that also installs Adafruit GFX and Adafruit BusIO.

## 3. Run the desk demo

1. Wire the screen: VCC to 3.3 V, GND to GND, SDA to GPIO 10, SCL to GPIO 9.
2. In Arduino IDE, choose **File > Open** and pick `firmware\desk-demo\desk-demo.ino` in your clone (by default `Documents\GitHub\Bakfiets-F26\firmware\desk-demo\desk-demo.ino`).
3. Choose **Tools > Board > esp32 > ESP32S3 Dev Module**.
4. Set **Tools > USB CDC On Boot > Enabled**.
5. Plug the board in using the USB-C port labelled **USB** (not the one labelled UART). Choose its COM port under **Tools > Port**.
6. Click **Upload**.
7. Wait about 10 seconds. The screen should show 50%, 36 km/h and PA 5. It's blank at first because the code plays the LED animation before it draws.

**Upload says "Failed to connect"?** Hold the **BOOT** button, tap **RST**, release BOOT, then click Upload again.
**No COM port?** Try another USB-C cable (some only charge), or, if you're on the port labelled UART, install the CP210x or CH340 USB driver.
**Blank screen?** Check the SDA and SCL wires, then change `SCREEN_ADDRESS` in the code to `0x3D`. The message "SSD1306 allocation failed" in Serial Monitor (at 9600 baud) means the ESP32 couldn't reserve memory for the screen; it's not a wiring fault.

More help: [ESP32 OLED tutorial for beginners](https://www.youtube.com/watch?v=u8g34BS8Ouw) (17 min) and the written [ESP32 + SSD1306 guide](https://randomnerdtutorials.com/esp32-ssd1306-oled-display-arduino-ide/).

## 4. Learn the basics

| Topic | Link |
| --- | --- |
| Addressable LEDs with FastLED | [Get started with WS2812B and FastLED](https://www.youtube.com/watch?v=JEwKKacCE2k) (30 min) |
| Timing without freezing the code | [millis() instead of delay()](https://www.youtube.com/watch?v=BYKQ9rk0FEQ) (14 min) |
| CAN bus | [CAN bus explained](https://www.youtube.com/watch?v=FqLDpHsxvf8) (CSS Electronics, 9 min) and the written [ESP32 CAN guide](https://lastminuteengineers.com/esp32-can-bus-tutorial/) |
| VESC basics | [VESC Tool 2024 setup](https://www.youtube.com/watch?v=YFl3VvZTRb0) (MBoards, 23 min) |
| PlatformIO (used by other Electrium repos) | [ESP32 in VS Code with PlatformIO](https://www.youtube.com/watch?v=F3oPVm2n-fk) (11 min) |

## 5. What exists

[`firmware/README.md`](../../firmware/README.md) lists the known bugs in the 2024 code and the other Electrium repos that already read a VESC.

## 6. Pick a first task

The desk demo (section 3) is your Stage 1; post a photo on [#12](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/12). Then pick a Stage 2 task in [ONBOARDING.md](../../ONBOARDING.md#firmware-onboarding).
