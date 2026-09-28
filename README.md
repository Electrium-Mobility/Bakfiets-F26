# Bakfiets F26

Electrium Mobility's electric cargo bike ("Bak Choy"), Fall 2026. This repo holds everything from the 2024 build and the 2025 co-op CAD, organized so a new member can find their part in a minute.

![2024 render of the bakfiets](docs/images/render-2024.png)

## New here?

**Open [ONBOARDING.md](ONBOARDING.md).** Everything you need is there, starting with a short to-do list at the top. Setup takes about 2 to 3 hours; try to finish it before the next Wednesday meeting (6:30 to 7:30 pm, in the Electrium bay). Questions go in your subteam's channel.

## What's in this repo

| Folder | What's inside | Start with |
| --- | --- | --- |
| [`mechanical/`](mechanical/) | All SolidWorks CAD | [`mechanical/README.md`](mechanical/README.md) |
| [`mechanical/cad-2025-coop/`](mechanical/cad-2025-coop/) | Newest model (May 2025), matches the partly built bike | `bakfiets_main_asm.SLDASM` |
| [`mechanical/cad-2024/`](mechanical/cad-2024/) | The 2024 design: frame, steering, kickstand, cargo box, welding jig, notching guides, FEA study | `Assem1.SLDASM` |
| [`electrical/`](electrical/) | The 2024 block diagram and notes on reusable boards | [`electrical/README.md`](electrical/README.md) |
| [`firmware/`](firmware/) | Display code, a ready-to-run desk demo, the CAN bus example | [`firmware/desk-demo/desk-demo.ino`](firmware/desk-demo/desk-demo.ino) |
| [`docs/setup/`](docs/setup/) | Extra setup detail and videos for each subteam | [`2-mechanical.md`](docs/setup/2-mechanical.md) |
| [`docs/term-projects.md`](docs/term-projects.md) | The main goals for the term, for after onboarding | |
| [`docs/reference-projects.md`](docs/reference-projects.md) | Other Electrium repos worth copying from | |
| [`docs/meetings/`](docs/meetings/) | Agenda and notes for each team meeting | [`2026-09-30.md`](docs/meetings/2026-09-30.md) |
| [`docs/diagrams/`](docs/diagrams/) | Onboarding path, bike overview, team structure, how to submit, term project map (with the scripts that draw them) | |
| [`docs/images/`](docs/images/) | Renders, CAD previews, photos | |
| [`docs/history/`](docs/history/) | Old README, website pages, and where every file came from | [`SOURCES.md`](docs/history/SOURCES.md) |

## Where the project stands

See [Where It Stands](ONBOARDING.md#where-it-stands) and [Open Questions](ONBOARDING.md#open-questions) in the onboarding guide. The main goals for the term are in [docs/term-projects.md](docs/term-projects.md).

## Rules for this repo

- Work on a branch and open a pull request. Don't push straight to `main`.
- Don't move or rename SolidWorks files inside `cad-2024/` or `cad-2025-coop/`. Assemblies find their parts by folder path, and moving files breaks them.
- Put new work in a new folder, for example `mechanical/cad-2026/` or `firmware/display-2026/`. Copy CAD with SolidWorks **Pack and Go**, and only one person edits a CAD file at a time.
