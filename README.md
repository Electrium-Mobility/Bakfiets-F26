# Bakfiets F26

Electrium Mobility's electric cargo bike ("Bak Choy"), Fall 2026. This repo holds everything from the 2024 build and the 2025 co-op CAD, organized so a new member can find their part in a minute.

![2024 render of the bakfiets](docs/images/render-2024.png)

## New here? Do these in order

**Start with [ONBOARDING.md](ONBOARDING.md).** It walks you from zero to your first contribution. Setup takes about 2 to 3 hours; try to finish it before the next Wednesday meeting (6:30 pm, workbay 1002). The short version:

1. **Make a GitHub account and join the Discord** ([invite](https://discord.gg/jggFVza4XR)). In the **Bakfiets F26** category, post your GitHub username in the **Github usernames** thread in #bakfiets-general so you can be added to the repo. You can keep going while you wait: the repo is public.
2. **Set up your computer** with the step-by-step guide for everyone: [docs/setup/1-everyone.md](docs/setup/1-everyone.md).
3. **Set up for your subteam:** [Mechanical](docs/setup/2-mechanical.md) · [Electrical](docs/setup/3-electrical.md) · [Firmware](docs/setup/4-firmware.md).
4. **Do your subteam's Stage 1** in [ONBOARDING.md](ONBOARDING.md) (open the bike, read a board, or run the desk demo), then **pick a Stage 2 task** from the table under it. Comment "I'll take this" on the issue and it's yours.
5. **After onboarding,** move on to the term projects in [docs/term-projects.md](docs/term-projects.md) (issues labelled `term project`).
6. **Questions** go in your subteam's channel. Who leads what is in [the everyone guide](docs/setup/1-everyone.md#5-how-the-team-is-run).

**Safety first:** don't weld, cut, grind or use the laser cutter, and don't touch a battery pack, until you've done the training listed in [the everyone guide](docs/setup/1-everyone.md#3-safety-training).

## What's in this repo

| Folder | What's inside | Start with |
| --- | --- | --- |
| [`mechanical/`](mechanical/) | All SolidWorks CAD | [`mechanical/README.md`](mechanical/README.md) |
| [`mechanical/cad-2025-coop/`](mechanical/cad-2025-coop/) | Newest model (May 2025), matches the partly built bike | `bakfiets_main_asm.SLDASM` |
| [`mechanical/cad-2024/`](mechanical/cad-2024/) | The 2024 design: frame, steering, kickstand, cargo box, welding jig, notching guides, FEA study | `Assem1.SLDASM` |
| [`electrical/`](electrical/) | The 2024 block diagram and notes on reusable boards | [`electrical/README.md`](electrical/README.md) |
| [`firmware/`](firmware/) | Display code, a ready-to-run desk demo, the CAN bus example | [`firmware/desk-demo/desk-demo.ino`](firmware/desk-demo/desk-demo.ino) |
| [`docs/setup/`](docs/setup/) | Step-by-step setup guides with videos | [`1-everyone.md`](docs/setup/1-everyone.md) |
| [`docs/term-projects.md`](docs/term-projects.md) | The main goals for the term, for after onboarding | |
| [`docs/reference-projects.md`](docs/reference-projects.md) | Other Electrium repos worth copying from | |
| [`docs/meetings/`](docs/meetings/) | Agenda and notes for each team meeting | [`2026-09-30.md`](docs/meetings/2026-09-30.md) |
| [`docs/diagrams/`](docs/diagrams/) | Onboarding path, bike overview, team structure, how to submit, term project map (with the scripts that draw them) | |
| [`docs/images/`](docs/images/) | Renders, CAD previews, photos | |
| [`docs/history/`](docs/history/) | Old README, website pages, and where every file came from | [`SOURCES.md`](docs/history/SOURCES.md) |

## Where the project stands

| Area | What exists | Next milestone |
| --- | --- | --- |
| Mechanical | SolidWorks model, welding jig, notching guides, one FEA study, a partly built frame | Record what is welded; rerun FEA with written load cases |
| Electrical | The 2024 block diagram (redrawn) and an antispark enclosure model; no schematics | Confirm the motor (#1); draft the power board schematic |
| Firmware | A screen and LED demo with fixed numbers | Show a real battery voltage and one working button |

### Open questions

The 2024 files disagree on a few basics. These are the answers we're working from until a check on the real bike says otherwise.

| Question | Our answer | How to check |
| --- | --- | --- |
| Which motor? | A 500 W hub motor with an FSESC 6.7 (VESC) controller, as the club website says. The 2024 README and crank-motor CAD point to a Bafang BBS02 mid-drive instead | Hub motor = a drum around a wheel's axle; BBS02 = a box at the pedals. [Issue #1](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/1) |
| Which microcontroller? | ESP32-S3. The display code's GPIO 9 and 10 don't work on a plain ESP32 | Read the chip label on the 2024 board, if it's still in the room |
| What happened to the 2024 electrical design? | Only the block diagram was saved, so the power board and wiring are designed fresh | Photograph anything still on the bike. [Issue #7](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/7) |
| How much of the frame is built? | Partly: the May 2025 CAD calls it "partially built" | List the welded joints and measure against the CAD. [Issues #2](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/2) and [#4](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/4) |

[ONBOARDING.md](ONBOARDING.md#open-questions) explains what changes in each plan if an answer turns out wrong.

The step-by-step onboarding, with first assignments per subteam and a glossary, is [ONBOARDING.md](ONBOARDING.md).

## Rules for this repo

- Work on a branch and open a pull request. Don't push straight to `main`.
- Don't move or rename SolidWorks files inside `cad-2024/` or `cad-2025-coop/`. Assemblies find their parts by folder path, and moving files breaks them.
- Put new work in a new folder, for example `mechanical/cad-2026/` or `firmware/display-2026/`. Copy CAD with SolidWorks **Pack and Go**, and only one person edits a CAD file at a time.
