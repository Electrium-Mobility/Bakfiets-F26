"""Pictures of the milled stopper on the head tube, and the bent-rod GIF with it fitted
in place of the welded strip. Usage: render_stopper.py [stills] [gif]
Output: views/stopper_*.png and views/stopper_*.gif"""
import sys
import pyvista as pv
import render as R
import gif_current as G
import stopper_milled as S

made, bump = S.parts(R.C.asm)
G.fixed.clear()
G.fixed.update({k: R.mesh(v, 0.2) for k, v in made.items()})
G.fixed.update({"bumper 1": R.mesh(bump[0], 0.3), "bumper 2": R.mesh(bump[1], 0.3)})
G.FIXED_COLOUR.update({"stopper block": "#2ca02c", "stop bar front": "#98df8a", "stop bar rear": "#98df8a"})

CAMS = {"right_front": [(1050, -420, 420), (700, -20, 380), (0, 0, 1)],
        "right_rear": [(380, -460, 470), (700, -20, 380), (0, 0, 1)],
        "below": [(840, -330, 120), (700, -20, 370), (0, 0, 1)]}

if __name__ == "__main__":
    args = sys.argv[1:] or ["stills", "gif"]
    if "stills" in args:
        for bar, tag in ((0.0, "straight"), (G.fork_to_bar(S.STOP_DEG), "right"), (G.fork_to_bar(-S.STOP_DEG), "left")):
            for name, cam in CAMS.items():
                p = pv.Plotter(off_screen=True, window_size=(1400, 1000))
                p.set_background("white")
                G.frame(p, bar)
                p.camera_position = cam
                p.screenshot(f"views/stopper_{name}_{tag}.png")
                p.close()
                print("saved", name, tag, flush=True)
    if "gif" in args:
        for g, cam in (("close_up", G.CAMS["close_up"]), ("head", CAMS["right_front"])):
            p = pv.Plotter(off_screen=True, window_size=(900, 600))
            p.open_gif(f"views/stopper_{g}.gif", fps=12)
            angles = G.sweep_angles(2.5, S.STOP_DEG)
            for a in angles:
                p.clear()
                p.set_background("white")
                G.frame(p, float(a))
                p.camera_position = cam
                p.write_frame()
            p.close()
            print("saved gif", g, len(angles), "frames", flush=True)
