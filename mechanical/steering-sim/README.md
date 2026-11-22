# Steering simulation

This code worked out the new steering in [docs/steering](../../docs/steering/README.md). Run it again whenever the frame or the parts change.

## Setting up

You need Python 3.11 or newer. In this folder, run:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
mkdir step views videos
```

The code reads the bike from `step\f26bakfiets_main_asm.step`. Make this file by opening `mechanical/cad-2026/f26bakfiets_main_asm.SLDASM` in SolidWorks and choosing *File > Save As > STEP*. It stays out of the repo because it's big and comes straight from the CAD.

## Running it

Run these in order. The first one only shows how the current steering behaves.

```
.venv\Scripts\python current_design.py
.venv\Scripts\python simple_jackshaft.py
.venv\Scripts\python final_check.py
.venv\Scripts\python render_offshelf.py
.venv\Scripts\python export_offshelf.py
```

`simple_jackshaft.py` takes about 10 minutes and `final_check.py` about 10 more. To change the stop angle, edit `STOP_DEG` in `jackshaft.py`. The sizes of the bought parts, the plate heights and the stop sit near the top of `offshelf.py`.

## What the files do

| File | What it does |
| --- | --- |
| `current_design.py` | Turns the current steering through every angle and shows where it jams |
| `linkage.py` | The maths for one arm, rod and arm turning together |
| `jackshaft.py` | The new steering and the rules it has to follow, such as staying under the box |
| `simple_jackshaft.py` | Tries shaft positions and arm lengths and keeps the one with the closest steering |
| `jackshaft_check.py` | Loads the bike and turns its parts to any steering angle |
| `offshelf.py` | Builds the bought parts: bearings, plates, U-bolts, hubs, arms, rod ends and the stop |
| `final_check.py` | Measures every gap between the new parts and the bike from full left to full right |
| `quick_check.py` | A faster check of the stop and the parts near the fork |
| `render.py` | Turns CAD parts into meshes for the pictures, and holds the colours |
| `render_offshelf.py` | Makes the pictures in `views`, the videos in `videos` and the animation for the docs |
| `export_offshelf.py` | Saves the new parts as `step\offshelf_parts.step` |
| `simple.npy`, `fork_spacer.npy` | The chosen sizes, which the other files read |
| `jackshaft_parts.step` | The new parts in place on the bike, to open in SolidWorks |
| `ExportStep.cs` | Optional. Saves SolidWorks files as STEP without opening the SolidWorks window. Instructions are in the first lines of the file |
