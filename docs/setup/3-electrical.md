# Setup for electrical

Do [Getting Started](../../ONBOARDING.md#getting-started) in the onboarding guide first. You need the safety training before battery work, but not for anything in this guide.

The steps you have to do are in [Electrical Stage 1](../../ONBOARDING.md#stage-1-read-a-real-board). This page repeats them with extra help, so you don't need to do anything twice.

## 1. Install KiCad 9

1. Download KiCad 9 from [kicad.org/download](https://www.kicad.org/download/). It's free.
2. Install with the default options, including the libraries.
3. Watch [KiCad 9.0 Getting Started, part 1](https://www.youtube.com/watch?v=0WCi1rhueH4) (DigiKey, 4 min) and continue through that series. For one video from schematic to finished board, try [Build your first PCB in KiCad 9](https://www.youtube.com/watch?v=moP6JxN7FWk) (16 min).

## 2. Your first hour: read a real board

1. In GitHub Desktop, choose **File > Clone repository > URL** and paste `Electrium-Mobility/anti-spark`.
2. In KiCad, choose **File > Open Project** and pick `Anti-Spark Switch.kicad_pro` in your `anti-spark` folder.
3. KiCad will say the project comes from an older version and offer to upgrade it. Click OK: that's expected. GitHub Desktop will then show those files as changed. Leave them, and don't commit them.
4. In the left panel, double-click `Anti-Spark Switch.kicad_sch` to open the schematic.
5. Find the three MOSFETs (Q1, Q2 and Q3, rated 100 V) and trace where the battery connects.

If you open the PCB, KiCad also warns that the `XT60PW-F` footprint library is missing. The 2023 designer kept it on their own computer, but it doesn't matter for reading the schematic.

## 3. Learn the basics

Before Stage 1 you only need the MOSFET video. Watch the rest when a task needs them.


| Topic | Video |
| --- | --- |
| Soldering | [Collin's Lab: Soldering](https://www.youtube.com/watch?v=QKbJxytERvg) (Adafruit, 5 min) |
| Multimeter | [How to use a multimeter](https://www.youtube.com/watch?v=SLkPtmnglOI) (SparkFun, 11 min) |
| Series and parallel cells | [Batteries in series vs parallel](https://www.youtube.com/watch?v=5lBDdcF6eAk) (3 min) |
| BMS | [BMS: properly protecting Li-ion packs](https://www.youtube.com/watch?v=rT-1gvkFj60) (GreatScott!, 13 min) |
| MOSFET as a switch | [Transistor (MOSFET) as a switch](https://www.youtube.com/watch?v=o4_NeqlJgOs) (GreatScott!, 6 min) |
| Buck converter | [DIY buck converter](https://www.youtube.com/watch?v=m8rK9gU30v4) (GreatScott!, 6 min) |
| VESC setup | [VESC Tool 2024: motor configuration and battery settings](https://www.youtube.com/watch?v=YFl3VvZTRb0) (MBoards, 23 min) |

## 4. What exists

[`electrical/README.md`](../../electrical/README.md) has the power flow diagram, explained step by step, and notes on which other Electrium boards you can reuse.

## 5. Pick a first task

Reading the anti-spark schematic (section 2) is your Stage 1. Post your notes on #8, then pick a Stage 2 task in [ONBOARDING.md](../../ONBOARDING.md#electrical-onboarding).
