# Bakfiets F26

Electrium Mobility's electric cargo bike ("Bak Choy"), Fall 2026. This repo holds everything from the 2024 build and the 2025 co-op CAD, organized so a new member can find their part in a minute.

![2024 render of the bakfiets](docs/images/render-2024.png)

## New here? Do these in order

1. **Make a GitHub account and join the Discord** ([invite](https://discord.gg/jggFVza4XR)). In the **Bakfiets F26** category, post your GitHub username in the **Github usernames** thread so you can be added to the org.
2. **Set up your computer** with the step-by-step guide for everyone: [docs/setup/1-everyone.md](docs/setup/1-everyone.md).
3. **Set up for your subteam:** [Mechanical](docs/setup/2-hardware.md) · [Electrical](docs/setup/3-electrical.md) · [Firmware](docs/setup/4-firmware.md).
4. **Pick a task** from the [Issues tab](https://github.com/Electrium-Mobility/Bakfiets-F26/issues). Anything labelled `good first issue` is meant for you. Comment "I'll take this" and it's yours.
5. **Questions** go in your subteam's thread in #bakfiets-general. Who leads what is in [the everyone guide](docs/setup/1-everyone.md#5-how-the-team-is-run).

**Safety first:** don't weld, cut, grind or use the laser cutter, and don't touch a battery pack, until you've done the training listed in [the everyone guide](docs/setup/1-everyone.md#3-safety-training).

## What's in this repo

| Folder | What's inside | Start with |
| --- | --- | --- |
| [`hardware/`](hardware/) | All SolidWorks CAD | [`hardware/README.md`](hardware/README.md) |
| [`hardware/cad-2025-coop/`](hardware/cad-2025-coop/) | Newest model (May 2025), matches the partly built bike | `bakfiets_main_asm.SLDASM` |
| [`hardware/cad-2024/`](hardware/cad-2024/) | The 2024 design: frame, steering, kickstand, cargo box, welding jig, notching guides, FEA study | `Assem1.SLDASM` |
| [`electrical/`](electrical/) | The 2024 block diagram and notes on reusable boards | [`electrical/README.md`](electrical/README.md) |
| [`firmware/`](firmware/) | Display code, a ready-to-run desk demo, the CAN bus example | [`firmware/desk-demo/desk-demo.ino`](firmware/desk-demo/desk-demo.ino) |
| [`docs/setup/`](docs/setup/) | Step-by-step setup guides with videos | [`1-everyone.md`](docs/setup/1-everyone.md) |
| [`docs/reference-projects.md`](docs/reference-projects.md) | Other Electrium repos worth copying from | |
| [`docs/images/`](docs/images/) | Renders, CAD previews, diagrams, photos | |
| [`docs/history/`](docs/history/) | Old README, website pages, and where every file came from | [`SOURCES.md`](docs/history/SOURCES.md) |

## Where the project stands

| Area | What exists | Next milestone |
| --- | --- | --- |
| Hardware | SolidWorks model, welding jig, notching guides, one FEA study, a partly built frame | Record what is welded; rerun FEA with written load cases |
| Electrical | A power flow diagram; nothing else survived on GitHub | Confirm the hub motor and VESC; draft the power board schematic |
| Firmware | A screen and LED demo with fixed numbers | Show a real battery voltage and one working button |

### Decisions on the open questions

These use the best evidence in the files. Each can change if the real bike says otherwise.

| Question | Decision | Why |
| --- | --- | --- |
| Which motor? | **500 W hub motor with an FSESC 6.7 (VESC) controller** | The sources conflict. The README (Feb 2024) names a Bafang BBS02 mid-drive, and the 2024 CAD has a crank motor. The club website names a specific part, the FSESC 6.7 VESC with a 500 W hub motor; that text was added in June 2024 and repeated in April 2025. We go with the website's more specific, more recent description. Confirm on the bike: [issue #1](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/1) |
| Which microcontroller? | **ESP32-S3** | The June 2024 website says ESP32-S3, and the display code's pins (GPIO 9 and 10) don't work on a plain ESP32, which wires them to its flash chip. The Nov 2024 CAN test used a plain ESP32 dev board |
| Where are the 2024 electrical files? | **Treat them as lost; design fresh** | Nothing was pushed to GitHub. Start from the reference boards in [electrical/README.md](electrical/README.md) |
| How much of the frame is built? | **Partly built** | The most recent note (May 2025 co-op CAD) says "partially built". Record exactly what's welded: [issue #2](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/2) |

The step-by-step onboarding, with first assignments per subteam and a glossary, is the [Bakfiets F26 Onboarding doc](https://claude.ai/code/artifact/b6004990-ae9d-4ec5-97b0-95172e4c6a2b) (also pinned in #bakfiets-general).

## Rules for this repo

- Work on a branch and open a pull request. Don't push straight to `main`.
- Don't move or rename SolidWorks files inside `cad-2024/` or `cad-2025-coop/`. Assemblies find their parts by folder path, and moving files breaks them.
- Put new work in a new folder, for example `hardware/cad-2026/` or `firmware/display-2026/`.
