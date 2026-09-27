# Setup for mechanical

Finish [Setup for everyone](1-everyone.md) first. Your files are in the `mechanical/` folder of your clone.

## 1. Get SolidWorks 2026

The team uses **SolidWorks 2026**, the version on the campus lab PCs. Files saved in 2026 can't be opened in older versions.

- **On campus:** the Engineering Computing labs Fulcrum, Helix, Lever and WEEF have SolidWorks 2026 ([lab software list](https://uwaterloo.ca/engineering-computing/computer-labs/lab-software)). The Sedra Student Design Centre also has a 14-seat CAD studio for teams.
- **On your own laptop:** SolidWorks sells a student licence ([solidworks.com/product/students](https://www.solidworks.com/product/students)). It runs on Windows only; on a Mac, use a lab PC.

First time? Watch [Beginners Guide to SOLIDWORKS: Your First Part](https://www.youtube.com/watch?v=qjtYqxNpj50) (SOLIDWORKS, 8 min).

## 2. Tell SolidWorks where the tube profiles are

The frame is built from custom tube shapes ("weldment profiles") stored in your clone. SolidWorks needs to know where they are, or the frame won't rebuild. This way needs no admin rights, so it also works on lab PCs.

1. Open SolidWorks and choose **Tools > Options > System Options > File Locations**.
2. In **Show folders for**, pick **Weldment Profiles**.
3. Click **Add** and choose your clone's `mechanical\cad-2025-coop` folder (the one that contains `bakfiets_weldment_profiles`).
4. Click **OK**, then **Yes** if asked to confirm.

## 3. Open the bike

1. In SolidWorks, choose **File > Open**.
2. Go to your clone's `mechanical\cad-2025-coop` folder and open `bakfiets_main_asm.SLDASM`.
3. If SolidWorks asks where a part is, point it at the same `cad-2025-coop` folder.

The parts are built around one master sketch, `bakfiets_master_sketch.SLDPRT`. To change the geometry, make a copy in `mechanical/cad-2026/` with **File > Pack and Go** (add a prefix so names don't clash) and work on the copy. Don't save files while they're open from `cad-2025-coop`: SolidWorks 2026 converts them on save. One person edits a CAD file at a time: say on your issue which files you're changing, because Git can't merge two edits to the same SolidWorks file.

If the frame still shows rebuild errors, copy the `bakfiets_weldment_profiles` folder into the default Weldment Profiles folder listed in the same File Locations dialog (this one needs admin rights).

## 4. Learn the frame tools

- Weldments (how the frame is built): [Introduction to Weldments](https://www.youtube.com/watch?v=nbMxA178ADM) (CAD Decoded, 15 min)
- FEA (checking the frame is strong enough): [Static analysis for beginners](https://www.youtube.com/watch?v=Ys0eT57DzT4) (CAD Hub, 28 min)
- Tube mitering (shaping tube ends to fit): [How to miter bicycle tubes with a hand file](https://www.youtube.com/watch?v=mqS2rbv58Zs) (Cobra Framebuilding, 12 min)
- TIG welding chromoly, to understand the process only: [Learn how to TIG weld 4130 tubing](https://www.youtube.com/watch?v=nQ3bRaoMv74) (Miller, 3 min)

## 5. Where the 2024 files are

| Need | File in your clone |
| --- | --- |
| Whole 2024 bike | `mechanical/cad-2024/Assem1.SLDASM` |
| Frame and its drawing | `mechanical/cad-2024/Frame 2.0.SLDPRT`, `mechanical/cad-2024/Frame 2.0-Sweep8.SLDDRW` |
| Welding jig | `mechanical/cad-2024/jig/Jig/JigV2.SLDASM` |
| Notching guides | `mechanical/cad-2024/notches/` |
| Steering | `mechanical/cad-2024/steering system/steeringAssembly.SLDASM` |

Every file is explained in [`mechanical/README.md`](../../mechanical/README.md). Don't move or rename anything in `cad-2024` or `cad-2025-coop`; save your work in `mechanical/cad-2026/` (create the folder if it's missing).

## 6. Pick a first task

First do Mechanical Stage 1 in [ONBOARDING.md](../../ONBOARDING.md#mechanical-onboarding) (open the bike and post a screenshot in the **#bakfiets-mech** channel), then pick a Stage 2 task there, such as #2 or #3.
