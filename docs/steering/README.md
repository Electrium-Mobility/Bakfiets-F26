# New steering for the Bakfiets

This page proposes a fix for the steering problems on [#25](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/25). The people on #25 and the mechanical leads still need to check it.

Every part is bought except two flat plates, which only need cutting and drilling. Nothing gets welded, and the frame stays as it is.

![The new steering from the front right, with the new parts in colour](images/close-up.png)

In the pictures, red is the rods and rod ends, blue is the turning shaft, green is the bearings, purple is the plates holding them, orange is the arms and black is the stops. The box and wheel are see-through so you see the parts behind them.

## The problem

The handlebars sit behind the cargo box and the fork sits in front of it. A straight rod between them would pass through the box, so the rod on the bike now bends to go under the box and then up.

![The current bent rod in red](images/current-rod.png)

Both ends of the rod sit in ball joints, so the rod spins freely around the yellow line between the two balls. A straight rod spinning on this line does no harm. Ours has its bend 220 mm off the line, so the middle of the rod swings around and the rod flexes every time you turn the handlebars. You feel this as play.

Nothing stops the handlebars from turning too far either. In the CAD the steering jams after 50° to the left, and to the right it keeps turning until the wheel faces sideways. These match the problems listed on #25.

## The fix

The bent rod becomes two straight rods, with a short turning shaft where the bend was.

![The steering turning from full right to full left](images/steering.gif)

When you turn the handlebars:

1. The handlebar arm swings. The bike already has this arm.
2. It pushes the lower rod, which runs flat under the box.
3. The lower rod turns the shaft, which runs alongside the front frame tube in two bearings.
4. An arm near the top of the shaft pushes the short upper rod.
5. The upper rod pushes the arm on the fork, which the bike also already has, and the wheel turns.

Both rods are straight, so they push and pull without flexing. A stop on the shaft holds the handlebars to about 36° each way, well short of where the steering would jam.

## The joints

| Handlebar end | Bottom arm |
| --- | --- |
| ![The rod end on top of the existing handlebar arm](images/handlebar-joint.png) | ![The bottom arm with the lower rod's rod end bolted on](images/bottom-joint.png) |

| Top arm and upper rod | Fork end |
| --- | --- |
| ![The top arm, upper rod and upper bearing](images/top-joint.png) | ![The rod end on top of the existing fork arm](images/fork-joint.png) |

Both rods are M10 threaded rod with a rod end screwed onto each end. A rod end is a ring with a swivel ball inside, and a bolt goes through the ball into the end of an arm. Turning a rod end on its thread changes the rod's length, and you set the wheel straight this way.

The two rod ends on the existing arms bolt through the holes the old ball joints used. Both stand on a spacer on top of their arm. The handlebar spacer is 14 mm, which puts the ball where the old one was. The fork spacer is 21 mm, which lifts the ball 50 mm above the old one so the upper rod clears the top of the fork.

## The bearings and the stop

| Lower bearing and stop | Upper bearing |
| --- | --- |
| ![The lower bearing plate with the stop](images/stop.png) | ![The upper bearing plate under the top arm](images/upper-bearing.png) |

The shaft turns in two pillow block bearings. Both bolt onto a flat plate, and two U-bolts hold the plate against the side of the frame tube. In the middle of its height the front of the cargo box comes within about 35 mm of the frame tube. So one bearing sits low, just above the bend in the frame, and the other sits above the box, just under the top arm.

The stop is a shaft collar with a bolt sticking out of it. On full lock this bolt hits one of two bolts screwed into the lower plate. Both of those wear a rubber sleeve.

| Full left | Full right |
| --- | --- |
| ![The stop on full left](images/full-left.png) | ![The stop on full right](images/full-right.png) |

## More views

| From the right side | From the front and right |
| --- | --- |
| ![From the right side](images/side.png) | ![From the front and right](images/front-right.png) |

| From behind and above | From underneath |
| --- | --- |
| ![From behind and above](images/rear-right-high.png) | ![From underneath](images/underneath.png) |

![Close-up of the lower bearing](images/lower-bearing.png)

## Parts list

| Part | How many | Notes |
| --- | --- | --- |
| 12 mm steel shaft | 1 | Cut to about 500 mm |
| KP001 pillow block bearing, 12 mm bore | 2 | |
| 12 mm clamping hub with a flange | 2 | Holds the arms on the shaft. A small flange gives more room near the frame tube |
| Steel flat bar, 25 × 6 mm | About 250 mm | Two arms, about 120 and 115 mm long, drilled through both ends |
| M10 rod end, female thread | 4 | Replaces the two old ball joints, plus two for the new arms |
| M10 threaded rod | About 450 mm | About 400 mm for the lower rod and a short piece for the upper rod |
| M10 nuts | 4 | Lock the rod ends once the length is set |
| M8 U-bolts for a 44.5 mm (1¾") tube | 4 | Two for each plate |
| Steel or aluminium plate, 6 mm | 2 | 76 mm wide, about 107 and 61 mm long. The only made parts. Cut and drill |
| 12 mm shaft collar with an M6 set screw hole | 1 | Swap the set screw for an M6 × 45 bolt. It becomes the stop pin |
| M8 × 50 bolts with rubber sleeves | 2 | Screw into the lower plate as the stops |
| Steel tube spacers, 14 mm and 21 mm long | 2 | With longer bolts, under the rod ends on the existing arms |

The CAD also has a stopper bracket on the head tube with two rubber bumpers. This version leaves it out, because the stop sits on the shaft. The bracket would need welding to the frame.

[`jackshaft_parts.step`](../../mechanical/steering-sim/jackshaft_parts.step) has all the new parts in place on the bike, to open in SolidWorks.

## Sizes

Heights are measured up from the centre of the frame's main tube.

| Part | Size |
| --- | --- |
| Turning shaft | Runs alongside the front frame tube, leaning the same way, 45 mm to the right of the tube's centre |
| Bottom arm | 90 mm from the shaft to the rod end's ball, pointing right |
| Top arm | 85 mm from the shaft to the rod end's ball, pointing right |
| Lower rod | About 480 mm between ball centres. Set the exact length by turning the rod ends |
| Upper rod | About 100 mm between ball centres |
| Lower bearing plate | From 20 to 120 mm up, with the bearing 52 mm up |
| Upper bearing plate | From 305 to 362 mm up, with the bearing 333 mm up |
| Spacers | 14 mm on the handlebar arm, 21 mm on the fork arm |

## How well it steers

The wheel turns almost as far as the handlebars. Near the stops the two drift apart, by less than 5°.

| Handlebars | Wheel |
| --- | --- |
| 35° left | 30° left |
| 20° left | 18° left |
| Straight | Straight |
| 20° right | 20° right |
| 35° right | 38.5° right |

## Does anything hit?

A program turned the real wheel and fork from the CAD through the whole range and measured the gap between every new part and the bike. These are the closest.

| What | Closest gap | When |
| --- | --- | --- |
| Top arm's hub and frame tube | 3 mm | 25° left |
| Lower bearing plate and cargo box | 6 mm | All the time |
| Back stop bolt and cargo box | 7 mm | All the time |
| Lower bearing and cargo box | 7.5 mm | All the time |
| Lower rod and frame | 9 mm | Full right |
| Upper rod and top of the fork | 10 mm | 20° right |

Every other gap is 10 mm or more.

## Before building

- All of this comes from the CAD. Measure the real bike first, mainly the angle of the front frame tube and where the front of the box sits. The plates and the back stop bolt have only 6 mm to spare.
- The top arm's hub passes 3 mm from the frame tube. A hub with a smaller flange gives more room.
- Check the pillow block's centre height. The shaft sits about 46 mm from the frame tube's centre, so the plate plus the block's centre height has to come to about 24 mm.
- Nobody has checked yet whether the lower rod comes near the rider's feet.

## Building it in SolidWorks

The parts are simple, so you draw them from the tables above, with `jackshaft_parts.step` open beside them for reference.

To make the assembly turn when you drag the handlebars:

- Give the shaft, the handlebar post and the fork a concentric mate with whatever they turn in, so they only turn.
- On both ends of a rod, make the centre of the rod end's ball coincident with the centre of its bolt hole in the arm.
- Add an angle limit of 36° each way on the handlebars, or model the stop pin and bolts.

Then turn on *Collision Detection* while dragging to check the same gaps as the table above.

## How this was worked out

The 11 Nov assembly (`mechanical/cad-2026/f26bakfiets_main_asm.SLDASM`) was exported from SolidWorks and loaded into a Python CAD library called build123d. One program tried thousands of shaft positions and arm lengths, and kept the layout where the wheel follows the handlebars most closely. A second one turned the real bike parts through every angle to check the gaps, and a third placed the bought parts and the stop. The code, with instructions for running it again, is in [`mechanical/steering-sim`](../../mechanical/steering-sim/README.md).
