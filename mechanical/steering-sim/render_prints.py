"""One picture of the five print files laid out, for the build document."""
import glob, os
import pyvista as pv
pv.OFF_SCREEN = True
files = ["handlebar disc", "fork disc", "handlebar bracket, lower", "handlebar bracket, clamp cap", "fork bracket"]
p = pv.Plotter(off_screen=True, window_size=(1800, 700), shape=(1, 5), border=False)
for i, n in enumerate(files):
    p.subplot(0, i)
    p.set_background("white")
    m = pv.read(f"step/print/{n}.stl")
    p.add_mesh(m, color="#ff9f1c" if "disc" in n else "#d62728", smooth_shading=False)
    p.add_text(n, position="upper_edge", font_size=11, color="black")
    p.view_isometric()
    p.camera.azimuth = 20
    p.reset_camera()
p.screenshot("views/print_parts.png")
print("saved")
