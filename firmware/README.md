# Firmware

Setup steps and the desk demo are in [docs/setup/4-firmware.md](../docs/setup/4-firmware.md).

| Folder | What it is | Status |
| --- | --- | --- |
| [`desk-demo/`](desk-demo/) | **Start here.** The 2024 display code as a ready-to-open Arduino sketch, with the LED pin moved off GPIO 9 | Should run on an ESP32-S3 with an SSD1306 OLED; the first hardware test is #12 |
| [`display-2024/`](display-2024/) | The original 2024 code (`main.cpp`) and the hand-drawn screen layout | Fixed numbers only; kept unchanged for reference |
| [`can-twai-2024/`](can-twai-2024/) | Two ESP-IDF projects based on Espressif's TWAI (CAN) example, one with an OLED drawn with LVGL (Nov 2024). The folder names are reversed: the "receiver" is the board that transmits | Fixed values on screen (60% and 18); targets a plain ESP32 |
| [`simulator-2024/`](simulator-2024/) | A Rust desktop mock-up of the 128x64 screen | Optional; setup notes are for macOS |

![Screen layout](display-2024/display-prototype.jpeg)

## What the 2024 display does

- SSD1306 128x64 OLED over I2C (SDA GPIO 10, SCL GPIO 9) shows battery %, speed in km/h and pedal-assist level
- A 125-LED WS2813 strip plays a right-turn sweep with FastLED (a left-turn function exists but is never called)
- Every value is fixed in code: battery 50%, 36 km/h, PA 5. Nothing reads the motor, battery or buttons yet

## Known bugs in `display-2024/main.cpp`

1. The LED strip and the OLED clock both use GPIO 9. **Fixed in `desk-demo/`** (LED moved to GPIO 5).
2. The LED animations pause on `delay(10)` for every LED. Five sweeps run before each screen refresh, so the screen updates only every 8 to 9 seconds. Fix: use `millis()` and move one LED per loop.
3. `setup()` calls `loop()` directly.
4. A comment says it tests the left signal, but the code calls `rightTurn()`.
5. Small: the FastLED settings are defined after the library is included, so they do nothing; LED 62 belongs to both sweeps; `NUMFLAKES` and `logo_bmp` are unused.

## CAN code notes

- Pins: TX GPIO 14, RX GPIO 27. On an ESP32-S3, GPIO 27 is used by the flash and memory chips, so choose new CAN pins before moving this code to the S3.
- Build with ESP-IDF: see the README inside each folder.

## Missing: real motor data

The 2024 README says the team reverse-engineered the Bafang BBS02 motor protocol, but that code isn't in any Electrium repo. The current plan is a hub motor with a VESC controller (to be confirmed in [issue #1](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/1)), and other Electrium repos already read a VESC: see [docs/reference-projects.md](../docs/reference-projects.md#firmware).
