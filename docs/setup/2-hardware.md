# Setup for mechanical

Finish [Setup for everyone](1-everyone.md) first. Your files are in the `hardware/` folder of your clone.

## 1. Get SolidWorks 2026

The team uses **SolidWorks 2026**, the version on the campus lab PCs. Files saved in 2026 can't be opened in older versions.

- **On campus:** the Engineering Computing labs Fulcrum, Helix, Lever and WEEF have SolidWorks 2026 ([lab software list](https://uwaterloo.ca/engineering-computing/computer-labs/lab-software)). The Sedra Student Design Centre also has a 14-seat CAD studio for teams.
- **On your own laptop:** SolidWorks Design Standard for Students is free ([solidworks.com/product/students](https://www.solidworks.com/product/students)). It runs on Windows only; on a Mac, use a lab PC.

First time? Watch [Beginners Guide to SOLIDWORKS: Your First Part](https://www.youtube.com/watch?v=qjtYqxNpj50) (SOLIDWORKS, 8 min).

## 2. Tell SolidWorks where the tube profiles are

The frame is built from custom tube shapes ("weldment profiles") stored in your clone. SolidWorks needs to know where they are, or the frame won't rebuild. This way needs no admin rights, so it also works on lab PCs.

1. Open SolidWorks and choose **Tools > Options > System Options > File Locations**.
2. In **Show folders for**, pick **Weldment Profiles**.
3. Click **Add** and choose your clone's `hardware\cad-2025-coop` folder (the one that contains `bakfiets_weldment_profiles`).
4. Click **OK**, then **Yes** if asked to confirm.

## 3. Open the bike

1. In SolidWorks, choose **File > Open**.
2. Go to your clone's `hardware\cad-2025-coop` folder and open `bakfiets_main_asm.SLDASM`.
3. If SolidWorks asks where a part is, point it at the same `cad-2025-coop` folder.

Every part follows one master sketch, `bakfiets_master_sketch.SLDPRT`. Change the sketch and the whole bike updates.

## 4. Learn the frame tools

- Weldments (how the frame is built): [Introduction to Weldments](https://www.youtube.com/watch?v=nbMxA178ADM) (CAD Decoded, 15 min)
- FEA (checking the frame is strong enough): [Static analysis for beginners](https://www.youtube.com/watch?v=Ys0eT57DzT4) (CAD Hub, 28 min)
- Tube mitering (shaping tube ends to fit): [How to miter bicycle tubes with a hand file](https://www.youtube.com/watch?v=mqS2rbv58Zs) (Cobra Framebuilding, 12 min)
- TIG welding chromoly, to understand the process only: [Learn how to TIG weld 4130 tubing](https://www.youtube.com/watch?v=nQ3bRaoMv74) (Miller, 3 min)

## 5. Where the 2024 files are

| Need | File in your clone |
| --- | --- |
| Whole 2024 bike | `hardware/cad-2024/Assem1.SLDASM` |
| Frame and its drawing | `hardware/cad-2024/Frame 2.0.SLDPRT`, `hardware/cad-2024/Frame 2.0-Sweep8.SLDDRW` |
| Welding jig | `hardware/cad-2024/jig/Jig/JigV2.SLDASM` |
| Notching guides | `hardware/cad-2024/notches/` |
| Steering | `hardware/cad-2024/steering system/steeringAssembly.SLDASM` |

Every file is explained in [`hardware/README.md`](../../hardware/README.md). Don't move or rename anything in `cad-2024` or `cad-2025-coop`; save your work in `hardware/cad-2026/` (create the folder if it's missing).

## 6. Pick a first task

See the [mechanical issues](https://github.com/Electrium-Mobility/Bakfiets-F26/issues?q=is%3Aissue+is%3Aopen+label%3Ahardware). Good first ones: #2 (photograph the frame) and #3 (list the parts).
