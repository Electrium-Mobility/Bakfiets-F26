# Steering simulation

This code worked out the new steering in [docs/steering](../../docs/steering/README.md). Run it again if the frame or the parts change.

## Setting up

You need Python 3.11 or newer. In this folder, run:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
mkdir step views
```

The code reads the bike from `step\f26bakfiets_main_asm.step`. Make that file by opening `mechanical/cad-2026/f26bakfiets_main_asm.SLDASM` in SolidWorks and choosing *File > Save As > STEP*. It isn't in the repo because it's big and comes straight from the CAD.

## Running it

Run these in order. The first one only shows how the current steering behaves.

```
.venv\Scripts\python current_design.py
.venv\Scripts\python simple_jackshaft.py
.venv\Scripts\python refine.py
.venv\Scripts\python jackshaft_check.py
.venv\Scripts\python render.py
.venv\Scripts\python render_docs.py
```

`simple_jackshaft.py` takes about 10 minutes and `refine.py` about 40. To change the stop angle, edit `STOP_DEG` in `jackshaft.py`. To change the smallest gap allowed, edit `MIN_GAP` in `refine.py`.

## What the files do

| File | What it does |
| --- | --- |
| `current_design.py` | Turns the current steering through every angle and shows where it jams |
| `linkage.py` | The maths for one arm, rod and arm turning together |
| `jackshaft.py` | The new steering and the rules it has to follow, such as staying under the box |
| `simple_jackshaft.py` | Tries shaft positions and arm lengths and keeps the one that steers best |
| `refine.py` | Tries arm heights and spacer lengths against the real bike parts and keeps the one with the most room |
| `jackshaft_check.py` | Measures every gap from full left to full right and saves the new parts as `step\jackshaft_parts.step` |
| `render.py`, `render_docs.py` | Make the pictures and the animation in `views` |
| `simple.npy`, `fork_spacer.npy` | The chosen sizes, which the other files read |
| `jackshaft_parts.step` | The new parts in place on the bike, to open in SolidWorks |
| `ExportStep.cs` | Optional. Saves SolidWorks files as STEP without opening the SolidWorks window. Instructions are at the top of the file |
