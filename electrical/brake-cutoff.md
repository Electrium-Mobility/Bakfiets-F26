# Brake motor cut-off

This page explains how the motor stops when someone pulls a brake lever, what to buy, how to wire it and how to test it. It goes with [#40](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/40). Prices were read in November 2026.

This is a plan, and the circuit hasn't been built yet. The sensor's wiring still has to be confirmed, so do step 1 of the build before connecting anything.

Why we need it: Ontario requires the motor to stop when the brakes are applied ([O. Reg. 369/09](https://www.ontario.ca/laws/regulation/090369), section 3(2)). It has to work before the first ride. The bench test doesn't need it.

Why it needs extra parts: the levers we're ordering, a Tektro RS360A pair, are plain mechanical levers with no switch inside. Store-bought e-bikes usually have a switch built into the lever and a brake plug on the controller. Our VESC motor controller has no brake plug, so we add a sensor to each brake and wire it to one of the controller's input pins.

How it works: pulling a brake closes a switch, which connects 3.3 V to a signal wire. That wire goes to ADC2, an input pin on the controller's COMM port. The VESC firmware has a kill switch setting called ADC2 High, which stops the motor whenever ADC2 is above 1.65 V ([firmware source](https://github.com/vedderb/bldc/blob/master/timeout.c)). When the brake is released, a 10k resistor pulls the signal back to 0 V and the motor can run again.

![Brake cut-off wiring: controller 3.3 V through two sensors to a signal wire, which goes to ADC2 and later the ESP32, with a 10k resistor to ground](diagrams/brake-cutoff-wiring.png)

| Brake | Signal wire | Motor |
| --- | --- | --- |
| Both released | 0 V | Can run |
| Either pulled | 3.3 V | Stops |

The two sensors are wired side by side, so either brake sets it off. The 10k resistor is required. An unconnected ADC2 can float to a random voltage, and [one builder measured 1.2 V](https://foil.zone/t/magnet-operated-kill-switch/15715/25), which is close to the 1.65 V trigger.

There are two separate cables at each brake. The brake cable runs from the lever, through the sensor and inside its housing to the caliper, and it stops the wheel the same way it would without the sensor. The sensor's own wire carries the signal to the controller, and it stops the motor.

![Route of the brake cable from the lever through the sensor to the caliper, and the sensor wire through a Higo plug and pigtail to the motor controller](diagrams/brake-sensor-route.png)

What to buy:

| Part | Qty | Cost | Notes |
| --- | --- | --- | --- |
| [Grin Inline Cable Cutoff Sensor, 4-pin Higo](https://ebikes.ca/inline-cable-cutoff-sensor.html) | 2 | CA$21 each + shipping | Made for standard mechanical levers. The cable passes through it, so the housing may need to be cut shorter |
| 4-pin female Higo pigtail, the short cable that mates with the sensor's plug | 2 | Not picked yet | Check the plug genders match before buying |
| 10k resistor | 1 | Check the bay | |
| Thin wire and a plug for the COMM port | 1 set | Check the bay | The plug type depends on the controller model |

The sensor's wire is 50 cm and ends in a blue Higo plug. A Higo plug is a small waterproof round connector common on e-bikes. The controller will be further than 50 cm from the handlebars, so the pigtail side needs extra wire. Measure this once the controller's position on the frame is known, and include it in the wiring harness ([#20](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/20)).

Before building, we need two things from VESC Tool:

- The controller's model, which tells us where 3.3 V, ADC2 and GND are on the COMM port ([#38](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/38)).
- The firmware version. The kill switch was [added in June 2021](https://github.com/vedderb/bldc/commits/master/timeout.c), so older firmware needs updating first.

Build it on a breadboard first, with the battery unplugged whenever you change a wire.

1. Confirm the sensor is a plain switch. Grin doesn't publish the pinout. Email info@ebikes.ca, or set a multimeter to continuity and find the two pins on the plug that connect only when the sensor is triggered. If no pair of pins does this, the sensor needs power and has its own output, so stop here and measure that output before connecting it. It must stay at or below 3.3 V.
2. Connect one sensor using the table below, and leave the ESP32 and second sensor off for now.
3. Check with a multimeter that the signal row reads 0 V, then 3.3 V when the sensor is triggered.
4. Power up, connect VESC Tool and watch the ADC2 voltage in its live data while triggering the sensor.
5. In App Settings, set Kill Switch Mode to ADC2 High and write the configuration. Menu names can vary a little between versions.
6. With the back wheel lifted and the current limits low, spin the motor and trigger the sensor. The motor should stop, and it should only restart once the sensor is released.
7. Add the second sensor and repeat step 6 with each brake.
8. Add the ESP32 and read the signal for the brake light (see below).

| From | To |
| --- | --- |
| Controller 3.3 V | Red breadboard rail |
| Controller GND | Blue breadboard rail |
| Front sensor, switch pin 1 | Red rail |
| Front sensor, switch pin 2 | Signal row |
| Rear sensor, switch pin 1 | Red rail |
| Rear sensor, switch pin 2 | Signal row |
| 10k resistor | Signal row to blue rail |
| Signal row | Controller ADC2 |
| ESP32 GND (step 8) | Blue rail |
| Signal row (step 8) | ESP32 input pin, through a 1k resistor |

Breadboards are for the bench only, because jumper wires can shake loose on a bike. Once it works, move the circuit to perfboard with screw terminals.

The ESP32 only reads the signal for the brake light. The signal is 0 V or 3.3 V, so it's safe for the ESP32-S3, whose pins aren't rated for 5 V. The 1k resistor protects the pin if the ESP32 is off while the controller is on. The cut-off doesn't depend on the ESP32. The firmware also [ignores commands while the kill switch is active](https://github.com/vedderb/bldc/commits/master/timeout.c), so the ESP32 shouldn't be able to restart the motor during braking. Confirm this during testing once the CAN link works.

Before every ride, lift the back wheel, spin the motor, and pull each brake to confirm the motor stops. This matters because of how the circuit fails: if a wire breaks or a plug comes loose, the signal stays at 0 V and the motor keeps running when you brake. The brakes themselves still work, but the cut-off doesn't.

A later version can fix this with switches that stay closed until you brake, wired one after the other, with Kill Switch Mode set to ADC2 Low. Then a broken wire stops the motor too. The Grin sensor's switch type decides whether that's possible with these parts.

Other options we looked at:

| Option | Why it isn't the first choice |
| --- | --- |
| [Grin magnetic sensor](https://ebikes.ca/magnetic-cutoff-hg4.html), CA$21 | Leaves the cable alone, but needs room on the lever, which hasn't been checked on the RS360A |
| Levers with a built-in switch | Closest to a store-bought e-bike and simple to wire. They have to suit our long-pull Shimano caliper, and we haven't confirmed one that does |
| Reed switch or microswitch on the lever | Cheapest, but we'd have to design the mount ourselves and make it trigger every time |
| [Spintend ADC adapter](https://spintend.com/products/ewheel-adc-adapter-v3-for-diy-ebike-escooter-with-vesc), US$36 | Sold out in November 2026. It also overlaps with what the ESP32 is planned to do |
| ADC2 brake modes in VESC Tool | These are for variable braking, and [forum reports](https://forum.esk8.news/t/analog-throttle-brake-adc2-does-not-cut-power-to-the-throttle-what-is-wrong/8405) say they subtract from the throttle without fully cutting it |

Still open:

- The controller's model and COMM pinout ([#38](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/38)).
- The sensor's pinout and whether it's a plain switch.
- Which Higo pigtail to buy, and how much extra wire the harness needs.
- Which ESP32 input pin to use (firmware).
