# LED strip desk test (21 Nov)

On 21 Nov we got the 1 m strip from the bay to play a moving rainbow from an ESP32-S3 DevKitC-1. It was powered from a laptop over USB, with no power board and no extra parts. This page covers step 2 of [#72](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/72). The power board test and the current measurement are still to do.

## Parts

- ESP32-S3 DevKitC-1 (ESP32-S3-WROOM-1 module)
- The 1 m WS2812B strip from the bay, 144 LEDs
- A breadboard, three jumper wires and a micro-USB data cable

## Wiring

| Board pin | Strip pad |
| --- | --- |
| 5V | 5V |
| GND | GND |
| GPIO 5 | DIN |

![The board on a breadboard, wired to the strip](strip-breadboard.svg)

<img src="photos/03-board-on-breadboard.jpg" alt="The DevKitC-1 on the breadboard with the micro-USB cable in the USB port and the strip's wires on the pins" width="360">

The board sits across the middle gap of the breadboard, so its pins fill rows b and i. The jumper wires go into row a, directly above the pins. On a clone board the pins can be in a different order, so go by the names printed next to the pins.

Data has to go in at the strip's DIN end, which is the end the printed arrows point away from. On our strip the black 3-pin plug was on the other end, where the arrows point towards it, so we wired to the DIN end instead.

## Uploading the code

The code is [`firmware/strip-test/strip-test.ino`](../../firmware/strip-test/strip-test.ino). It needs the FastLED library, which you can install from *Sketch > Include Library > Manage Libraries*.

1. Plug the cable into the board's **USB** port.
2. Choose *Tools > Board > esp32 > **ESP32S3 Dev Module***.
3. Under *Tools > Port*, choose the port that appears when the board is plugged in. It was COM7 on the laptop we used.
4. Click Upload. It worked when the log ended with "Hash of data verified" and "Hard resetting via RTS pin". If the strip stays dark after that, press RESET on the board once.

Since the strip runs from USB, the code limits it to 400 mA and brightness 30. At full white, 144 LEDs can draw over 8 A.

## Result

The first upload had `NUM_LEDS` set to 60, so only the first 60 LEDs lit. The sketch in the repo is now set to 144.

<img src="photos/01-first-60-leds-lit.jpg" alt="The first 60 LEDs of the strip showing a rainbow on the bench" width="420"> <img src="photos/02-whole-strip-lit.jpg" alt="The strip held up with the rainbow running along it, next to the breadboard" width="300">

## Cutting and soldering

After the test we cut the strip into four pieces of 36 LEDs (25 cm), one bar for the front and one for the back, plus two side pieces. The front and back bars will show the turn signals as a sweep across the bar. Jack soldered wires and plugs onto two of the pieces the same night, and we made long red, black and green extension cables to run from the ESP32 to the lights. Finishing the other pieces is [#79](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/79), and the code for all four is [#80](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/80).

<img src="photos/07-cut-36-led-piece.jpg" alt="A cut 36-LED piece of the strip on the bench" width="420"> <img src="photos/06-piece-in-helping-hands.jpg" alt="A cut piece held in the helping hands at the soldering station" width="420">

<img src="photos/04-two-soldered-pieces.jpg" alt="Two pieces with red, white and green wires and black plugs soldered on" width="300"> <img src="photos/05-soldering-station.jpg" alt="The soldering station with the helping hands and the fume extractor" width="420">

<img src="photos/08-extension-cable.jpg" alt="The extension cables with white tape markers, laid out on the bench" width="300"> <img src="photos/09-extension-cable-length.jpg" alt="An extension cable held out across the floor to show its length" width="300">

## Problems we hit

- **No COM port on the UART port.** Windows saw the board's CP2102N chip, but had no driver for it (error 28 in Device Manager). The **USB** port works without a driver on Windows 11. To use UART, install the Silicon Labs CP210x driver.
- **Wrong board selected.** The IDE had ESP32S31 Dev Module selected, which is a different chip. ESP32S3 Dev Module, the plain one, is the right choice. Avoid the "Octal (WROOM2)" entry too.
- **Slow first build.** The first build compiles the ESP32 core and FastLED from scratch, which took several minutes. Builds after that took seconds.
- **Upload stuck on "Connecting...".** Hold BOOT, tap RESET, release BOOT, then upload again.

## Next

- Test the bay power board on the bench supply, then run the strip from it ([#72](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/72), step 1).
- Measure the strip's current at the brightness we plan to use, and post the number on #72.
- Plan where to cut the turn signal and brake light pieces once the light spots are measured on the bike ([#53](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/53)).
