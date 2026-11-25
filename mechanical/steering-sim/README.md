# Steering simulation

This code worked out the steering designs in [docs/steering](../../docs/steering/README.md). Run it again whenever the frame or the parts change.

## Setting up

You need Python 3.11 or newer. In this folder, run:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
mkdir step views videos
```

The code reads the bike from `step\f26bakfiets_main_asm.step`. Make this file by opening `mechanical/cad-2026/f26bakfiets_main_asm.SLDASM` in SolidWorks and choosing *File > Save As > STEP*. It stays out of the repo because it's big and comes straight from the CAD.

`current_design.py` turns the current bent rod through every angle and shows where it jams. `gif_current.py` makes GIFs of it.

## Jackshaft

```
.venv\Scripts\python simple_jackshaft.py
.venv\Scripts\python final_check.py
.venv\Scripts\python render_offshelf.py
.venv\Scripts\python export_offshelf.py
```

`simple_jackshaft.py` takes about 10 minutes and `final_check.py` about 12 more. To change the stop angle, edit `STOP_DEG` in `jackshaft.py`. The sizes of the bought parts, the plate heights, the stop and the rod end bolt directions sit near the top of `offshelf.py`.

| File | What it does |
| --- | --- |
| `linkage.py` | The maths for one arm, rod and arm turning together |
| `jackshaft.py` | The jackshaft layout and the rules it has to follow, such as staying under the box |
| `simple_jackshaft.py` | Tries shaft positions and arm lengths and keeps the one with the closest steering |
| `jackshaft_check.py` | Loads the bike and turns its parts to any steering angle |
| `offshelf.py` | Builds the bought parts and the bent arm tabs, with the rod end bolts set square to their rods |
| `final_check.py` | Measures every gap between the new parts and the bike from full left to full right |
| `shank_check.py` | Checks the rod end shanks and threaded rods against the tabs they bolt to |
| `quick_check.py` | A faster check of the stop and the parts near the fork |
| `render.py` | Turns CAD parts into meshes for the pictures, and holds the colours |
| `render_offshelf.py` | Makes the pictures in `views`, the videos in `videos` and the GIFs for the docs |
| `export_offshelf.py` | Saves the new parts as `step\offshelf_parts.step` |
| `simple.npy`, `fork_spacer.npy` | The chosen sizes, which the other files read |
| `jackshaft_parts.step` | The new parts in place on the bike, to open in SolidWorks |

## Cable

```
.venv\Scripts\python cable_check.py
.venv\Scripts\python stop_check.py
.venv\Scripts\python render_cable.py
.venv\Scripts\python gif_cable.py
.venv\Scripts\python export_prints.py
```

`cable_check.py` takes about 45 minutes and prints DONE when it finishes. The disc sizes, bracket sizes and housing route sit near the top of `cable.py`.

| File | What it does |
| --- | --- |
| `cable.py` | Builds the discs, brackets, spacers, cables and housings |
| `route_opt.py` | Searches for the shortest housing route clear of the bike. Its result is typed into `cable.py` |
| `cable_check.py` | Measures every gap between the new parts and the bike from full left to full right |
| `stop_check.py` | Finds where the stop tab on the fork disc meets the fork bracket |
| `render_cable.py`, `gif_cable.py` | Pictures and GIFs of the cable steering. `gif_cable.py video` makes MP4s |
| `export_prints.py`, `render_prints.py` | STL files of the printed parts, and a picture of them |
| `cable_parts.step` | The new parts in place on the bike, to open in SolidWorks |

## Stopper for the bent rod

```
.venv\Scripts\python stopper_milled.py
.venv\Scripts\python stopper_milled_check.py
.venv\Scripts\python stopper_strength.py
.venv\Scripts\python stopper_drawings.py
.venv\Scripts\python render_stopper.py
```

`stopper_milled_check.py` takes about a minute.

| File | What it does |
| --- | --- |
| `stopper.py` | An earlier printed version. Its helpers and the bumper positions are still used |
| `stopper_milled.py` | Builds the clamp block and the two stop bars, and saves them as STEP files in `step` |
| `stopper_milled_check.py` | Measures every gap from full left to full right, with the rod spun about its ball joints |
| `stopper_strength.py` | Bolt, bar and clamp loads for a 100 N·m pull into a stop |
| `stopper_drawings.py` | The shop drawings, `views\stopper_drawings.pdf` |
| `render_stopper.py` | Pictures and GIFs of the stopper |
| `stopper_block.step`, `stop_bar_front.step`, `stop_bar_rear.step` | The three parts, in the same coordinates as the bike |

## U-joint shafts

```
.venv\Scripts\python ujoint_space.py
.venv\Scripts\python ujoint_box_inside.py
.venv\Scripts\python ujoint_opt.py fixed3
.venv\Scripts\python ujoint_check.py fixed3
.venv\Scripts\python ujoint_render.py fixed3
```

Use `sketch` in place of `fixed3` for the layout as sketched. `ujoint_space.py` writes a 1 GB file, which stays out of the repo. `ujoint_opt.py` takes about 15 minutes. Its results are already saved as `ujoint_fixed3.npy` and `ujoint_sketch.npy`, so you skip the first three lines unless the bike changes.

| File | What it does |
| --- | --- |
| `ujoint_layout.py` | Joint sizes, ratings and the layout cases |
| `ujoint_space.py`, `ujoint_box_inside.py` | Point clouds of the bike and the inside of the box, for the fast search |
| `ujoint_opt.py` | Searches for the joint positions with the smallest bends |
| `ujoint_parts.py` | Joint and shaft shapes, and how the yokes turn |
| `ujoint_check.py` | Bends, the handlebar to fork table and every gap, from the full CAD |
| `ujoint_render.py`, `ujoint_explain.py` | Pictures and GIFs, and the GIF showing how the gearbox turns |

## Other files

`ExportStep.cs` is optional. It saves SolidWorks files as STEP without opening the SolidWorks window. Instructions are in the first lines of the file.
