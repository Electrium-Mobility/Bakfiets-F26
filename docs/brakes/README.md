# Brakes on the Bakfiets

The bike needs a working brake on each wheel before anyone rides it. This page collects what's known so far, with photos of the bike, as a starting point for the brakes task ([#32](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/32)).

## The short version

![Side view of the bike with the rear brake line and two example front brake line routes](images/bike-layout.svg)

- The front wheel already has a hydraulic disc brake, but its hose can't reach the handlebars. The handlebars sit in the middle of the bike and the front wheel is past the cargo box.
- The back wheel is the hub motor. It has no brake yet, and the motor and frame have no obvious place to mount one.
- Pulling either brake lever has to cut the motor.

Any setup has to stop the bike from 30 km/h within 9 m with a brake on each wheel, fit in roughly $220 to $260 shared with steering, and get approval if it changes the frame. The full list is under "Limits" below.

![Our frame, labelled](images/evidence-frame.jpg)

Our frame, with the parts this page talks about. Both wheels are still off the frame.

## What the brakes task should produce

Due Wed 21 Oct:
- a chosen front setup and a chosen rear setup, each with the reasons
- the parts and the specs they have to match (hose length and fittings, fluid type, levers with a cut-off switch)
- any frame change, flagged for approval
- how the brakes will be tested before anyone rides

## Front wheel

The front brake is a hydraulic disc brake. The lever pushes fluid down a hose to a caliper, which grips a metal disc (the rotor) bolted to the hub.

![A disc brake on another bike, labelled](images/disc-brake-reference.jpg)

What a disc brake looks like, on another bike. Ours is the same kind of brake.

Its hose is far too short for this layout (seen in the bay). A close photo of it would give its brand, model and fluid type, and those decide which parts are compatible.

The line has to reach the caliper at the front axle. Both the fork and the handlebar post turn when steering, so it has to bend at both ends. It could cross over the cargo box or follow the frame tubes under it (the two examples in the side view), and the steering design ([#25](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/25)) changes what works.

## Back wheel

### The motor has no disc mount

![The motor's cable side, labelled](images/evidence-motor-wheel.jpg)

A disc rotor bolts to a ring of six holes around the axle (or a splined Center Lock fitting), like in the disc brake photo above. Both sides of our motor look like plain covers. A close-up would confirm it.

![The motor's freewheel side, labelled](images/evidence-motor-side.jpg)

The threads next to the axle are for a freewheel (the rear gears), so the motor has to stay on the back wheel. The side covers are held on by the small screws around the edge.

### The frame has no rim brake mounts

![The rear of our frame, labelled](images/evidence-rear.jpg)

<img src="images/bare-bosses.jpg" alt="Bare bosses on another bike's seat stays, labelled" width="420">

V-brakes and cantilever brakes mount on bosses: two short posts on the seat stays, just below the rim (the second photo, from another bike). Our seat stays look like smooth tube. An old style caliper rim brake bolts through a bridge between the stays instead, and our stays look like they lack one too. The photo is low resolution, so it's worth checking by hand.

The rim has a silver band along its edge, which is usually a surface for rim brakes. It still needs a close look.

The dropout plates have several holes. Some may be for a rack, and the raised ones might be a disc tab. The spacing would tell: 51 mm apart for an IS disc mount, 74 mm for a post mount.

### Approaches people use

For a rear hub motor with no disc mount: bosses brazed or welded onto the seat stays, clamp-on boss plates ([some riders don't trust them](https://cyclechat.net/threads/v-brakes-fitting-to-a-frame-without-bosses.26234)), an adapter that bolts a rotor to the motor's cover screws, a disc tab if the frame turns out to have one, or a different motor with a disc mount. Drum and coaster brakes need a hub built for them, which rules them out here. Braking on the motor shell itself would put heat right next to the magnets, which weaken when hot.

## Open questions

Check in the bay first:
1. The front brake's brand, model, fluid type and hose fittings. A longer hose, a new lever or a bleed kit all have to match these, and mixing mineral oil with DOT fluid ruins the seals.
2. Close-ups of both sides of the motor. The current photos are taken from too far away to be sure, and a rotor mount would make a disc brake the easiest option for the back.
3. The seat stays, by hand. The photo is low resolution and the stays have tape on them. Bosses or a bridge would let a rim brake bolt straight on without changing the frame.
4. The silver band on the rim, up close. A rim brake needs a flat metal surface to grip, so this decides whether rim brakes are an option for the back at all.
5. The spacing of the raised dropout holes. 51 mm or 74 mm apart means a disc tab, which opens up a disc brake on the back with a rotor adapter on the motor.

Then work out:
1. Reuse the front brake with a longer hose, or replace it? Reusing is cheaper but ties every part to that brand. Replacing costs more but lets you pick parts that suit the long line.
2. Over the box or along the frame, and how long is the line then? The length decides which hose or cable to buy, and the route has to survive the fork and handlebar post turning, which depends on the steering design ([#25](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/25)).
3. How will the back wheel be braked, what does it cost, and does it change the frame? This is the hardest part and will take most of the budget. A frame change also needs approval, which takes time.
4. Which cut-off switch fits the levers you pick? The law requires one, and it has to plug into the controller's ADC2 input. Some levers have a switch built in, others need a separate sensor.
5. What load should the brakes be sized for (rider, cargo, battery and bike)? A loaded cargo bike is much heavier than a regular bike, and the brakes still have to stop it within 9 m from 30 km/h.

## Limits

- Ontario's rules ask for two independent brakes that apply force to each wheel, able to stop from 30 km/h within 9 m on level asphalt ([ontario.ca](https://www.ontario.ca/page/riding-e-bike)).
- Pulling a brake lever has to cut the motor (O. Reg. 369/09 s. 3(2)). On our bike that's a switch wired to the controller's ADC2 input ([#18](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/18), step 7).
- Steering and brakes share roughly $220 to $260 of the term's budget.
- Changing the frame (welding, drilling, filing) needs approval from a mechanical lead and the project lead.
- Parts go through the project lead once the specs they need to match are posted.
- Regen (the motor slowing the wheel) can't count as one of the two brakes. It stops working if the controller or battery cuts out, and fades away at low speed.

## Background

<details>
<summary>How a rim brake works on bosses</summary>

![A rim brake mounted on bosses, seen from behind the wheel (simplified)](images/rim-brake-on-bosses.svg)

Each brake arm pivots on a boss. The cable pulls the tops of the arms together, so the pads squeeze the rim.

<img src="images/v-brake-mounted.jpg" alt="A real V-brake mounted on bosses, labelled" width="420">

A real V-brake. The boss is hidden under the pivot bolt.

</details>

<details>
<summary>How the hub motor works</summary>

![Inside a direct-drive hub motor](images/hub-motor-inside.svg)

The axle and the stator (copper coils) are fixed to the frame and never turn. The shell, with magnets on its inside, spins around them and turns the wheel through the spokes. The controller sends current through the three phase wires in a rotating pattern, so the coils' magnetic field turns and drags the magnets along. Hall sensors on the stator tell the controller where the magnets are.

The stator pushes back on the axle as hard as it pushes the wheel, which is why the axle needs torque arms ([#31](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/31)).

</details>

<details>
<summary>Words used here</summary>

- **Caliper:** the part that squeezes. On a disc brake it grips the rotor.
- **Rotor:** the metal disc on the hub that a disc caliper grips.
- **Hydraulic:** the lever pushes fluid through a hose. Mineral oil and DOT fluid can't be mixed, because the wrong one ruins the seals.
- **Seat stays and chain stays:** the pairs of tubes that run to the rear axle, from under the seat and from the pedals.
- **Dropouts:** the plates at the back where the rear axle sits.
- **Freewheel:** the rear gears, which screw onto the hub.
- **Torque arm:** a bracket that stops a hub motor's axle from spinning in the dropouts.

</details>

## Image credits

- Disc brake photo: [StromBer, Wikimedia Commons](https://commons.wikimedia.org/wiki/File:BrakeDiskVR.JPG), CC BY 3.0. Resized and labelled.
- V-brake photo: [Keithonearth, from a photo by ArnoldReinhold, Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Linear_pull_bicycle_brake_highlighted.jpg), CC BY-SA 3.0. Resized and labelled.
- Bare bosses photo: [Bicycles Stack Exchange](https://bicycles.stackexchange.com/questions/87966/aside-from-brakes-what-items-can-be-mounted-to-v-brake-mounts), CC BY-SA. Resized and labelled.
- Frame and motor photos, labels and diagrams: Bakfiets F26.
