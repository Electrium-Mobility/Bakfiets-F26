# Brake motor cut-off

This page explains how the motor stops when someone pulls a brake lever, which parts we're using, how to wire it and how to test it. It goes with [#40](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/40). Updated 7 Nov 2026 after checking Electrium's spare parts in the bay.

This is a plan, and the circuit hasn't been built yet. The motor test on 4 Nov worked, so the controller, VESC Tool and motor are ready for this.

Why we need it: Ontario requires the motor to stop when the brakes are applied ([O. Reg. 369/09](https://www.ontario.ca/laws/regulation/090369), section 3(2)). It has to work before the first ride.

The bay has a lever with a cut-off built in. A switch or sensor inside the lever sends a signal down the thin wire whenever the lever is pulled, the same way store-bought e-bikes do it. We use that signal to stop the motor.

![Black lever with a thin cut-off wire ending in a yellow plug](photos/brake-parts-2026-11/1-lever-with-cutoff.jpg)

![The back of the same style of lever](photos/brake-parts-2026-11/2-lever-with-cutoff-back.jpg)

The cut-off wire ends in a yellow waterproof plug, known as a Higo or Julet plug.

![Close-up of the yellow plug](photos/brake-parts-2026-11/3-yellow-plug.jpg)

The rest of the parts from the bay are below. The plain levers have no cut-off, so they're only a backup.

![Two plain levers marked POWER, with no cut-off wire](photos/brake-parts-2026-11/4-plain-levers.jpg)

![Black brake housing, 2 m](photos/brake-parts-2026-11/5-housing.jpg)

![Inner brake wire, 2 m](photos/brake-parts-2026-11/6-inner-wire.jpg)

![Bag of ferrules, end caps and red cable protectors](photos/brake-parts-2026-11/7-small-parts.jpg)

Each brake uses one lever, one 2 m inner wire and one 2 m length of housing. The front line now runs along the box instead of along the frame, which is shorter than the 228 cm route we measured before. Measure both routes with a string, with the handlebars turned fully each way. The housing has to fit the route with some slack, and the inner wire has to be longer than the housing so it can reach the caliper.

There are two separate lines at each brake. The inner wire and housing stop the wheel. The cut-off wire stops the motor.

![Route of the inner wire and housing from the lever to the caliper, and the cut-off wire through the yellow plug and a pigtail to the motor controller](diagrams/brake-sensor-route.png)

The cut-off wire is short, so it needs a pigtail, which is a short cable with the other half of the yellow plug, plus extra wire to reach the controller. Include this in the wiring harness ([#20](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/20)).

The first job is finding out what kind of signal the lever sends. Look inside the yellow plug and count the pins, then test it with a multimeter.

![A multimeter on continuity mode connected to the pins of the yellow plug](diagrams/brake-plug-test.png)

| Result | What it means | What to do |
| --- | --- | --- |
| Two pins, and the meter beeps only when the lever is pulled | Plain switch that closes when you brake | Use the wiring below |
| Two pins, and the meter stops beeping when the lever is pulled | Plain switch that opens when you brake | Use the wiring below with Kill Switch Mode set to ADC2 Low. A broken wire then stops the motor too |
| Three pins, and the meter never beeps | Powered sensor | Find the power, ground and signal wires, give it 3.3 V and measure the signal. Set ADC2 High if the signal goes up when you brake, or ADC2 Low if it goes down. The signal must stay at or below 3.3 V |

Here's how the plain switch case works. Pulling a brake connects 3.3 V to a signal wire, which goes to ADC2, an input pin on the controller's COMM port. The VESC firmware has a kill switch setting called ADC2 High, which stops the motor whenever ADC2 is above 1.65 V ([firmware source](https://github.com/vedderb/bldc/blob/master/timeout.c)). When the lever is released, a 10k resistor pulls the signal back to 0 V.

![Wiring: controller 3.3 V through two levers to a signal wire, which goes to ADC2 and later the ESP32, with a 10k resistor to ground](diagrams/brake-cutoff-wiring.png)

The 10k resistor is required. An unconnected ADC2 can float to a random voltage, and [one builder measured 1.2 V](https://foil.zone/t/magnet-operated-kill-switch/15715/25), which is close to the 1.65 V trigger.

Before building, read the controller's model and firmware version in VESC Tool and post them on [#38](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/38). The model tells us where 3.3 V, ADC2 and GND are on the COMM port. The kill switch was [added to the firmware in June 2021](https://github.com/vedderb/bldc/commits/master/timeout.c), so older firmware needs updating first.

Build it on a breadboard first, with the battery unplugged whenever you change a wire.

1. Test the main idea with a 10k resistor and a jumper wire in place of the lever. Connect the resistor from ADC2 to GND, then set Kill Switch Mode to ADC2 High in App Settings. With the back wheel lifted and the current limits low, spin the motor and connect 3.3 V to ADC2. The motor should stop, and restart only once the wire is removed.
2. Test the yellow plug using the picture above.
3. Connect one lever using the table below.
4. Check with a multimeter that the signal row reads 0 V, then 3.3 V when the lever is pulled. Watch the same change on the ADC2 voltage in VESC Tool.
5. Repeat the motor test from step 1 using the lever.
6. Add the second lever and test each brake.
7. Add the ESP32 for the brake light.

| From | To |
| --- | --- |
| Controller 3.3 V | Red breadboard rail |
| Controller GND | Blue breadboard rail |
| Front lever, pin 1 | Red rail |
| Front lever, pin 2 | Signal row |
| Rear lever, pin 1 | Red rail |
| Rear lever, pin 2 | Signal row |
| 10k resistor | Signal row to blue rail |
| Signal row | Controller ADC2 |
| ESP32 GND (step 7) | Blue rail |
| Signal row (step 7) | ESP32 input pin, through a 1k resistor |

Breadboards are for the bench only, because jumper wires can shake loose on a bike. Once it works, move the circuit to perfboard with screw terminals.

The ESP32 only reads the signal for the brake light. The signal is 0 V or 3.3 V, so it's safe for the ESP32-S3, whose pins aren't rated for 5 V. The 1k resistor protects the pin if the ESP32 is off while the controller is on. The cut-off doesn't depend on the ESP32, and the firmware [ignores commands while the kill switch is active](https://github.com/vedderb/bldc/commits/master/timeout.c). Confirm that during testing once the CAN link works.

Fit the levers on the bike and check these before the first ride:

- The lever pulls enough cable to clamp the Shimano mechanical caliper firmly before the lever reaches the grip. Linear pull and short pull levers move different amounts of cable, and these levers haven't been tested with our calipers yet.
- The levers clamp onto our handlebars.
- With the back wheel lifted, pulling each brake stops the motor. Repeat this check before every ride. If the circuit uses a switch that closes when you brake, a broken wire leaves the motor running, although the brakes still work.

If we can't find a second lever with a cut-off, the second brake can use a plain lever with a [Grin inline sensor](https://ebikes.ca/inline-cable-cutoff-sensor.html), CA$21, wired the same way once we confirm its signal.

Still open:

- How many levers with a cut-off the bay has. The photos show one, labelled A01-R, and we need two.
- The number of pins on the yellow plug and what type of signal it sends.
- Which pigtail fits the yellow plug.
- The controller's model and COMM pinout ([#38](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/38)).
- The string measurements for both routes.
- Which ESP32 input pin to use (firmware).
