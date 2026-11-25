"""Hand strength numbers for the milled stopper, from the modelled geometry.

Design load: 100 N m of steering torque held by one bumper. For scale, a rider pulling
330 N on a grip 300 mm from the steering axis gives 100 N m. Loads are static; the
rubber bumpers soften a hit, which these numbers leave out.
"""
import numpy as np
import render as R
import stopper_milled as M
import stopper as S

T = 100.0                     # N m at the steering axis
AL_YIELD = 240.0              # MPa, 6061-T6 (276 typical, 240 minimum)
M6_PROOF = 16.1e3             # N, class 8.8 M6 proof load
MU = 0.2                      # clamp friction, aluminium on painted steel
PINCH_TORQUE = 6.0            # N m on each M6 pinch bolt, as for a stem clamp
K_NUT = 0.2                   # torque coefficient, dry thread

_, bump = M.parts(R.C.asm, local=True)
print(f"design load {T:.0f} N m at the steering axis\n")
for i, b in enumerate(bump):
    m, n = S.mount(b)
    r = np.hypot(m[0], m[1]) / 1000                       # contact radius, m
    F = T / r                                              # push on the bumper, N
    lever = (M.BLOCK_LO + M.POCKET - m[2]) - M.POCKET      # bumper centre to the block's underside, mm
    Mb = F * lever / 1000                                  # N m at the bar root
    Z = M.BAR ** 3 / 6                                     # mm3, square bar
    s_bar = Mb * 1000 / Z
    # Tipping about the bar's edge, held by the two bolts alone (pocket walls ignored).
    d_far, d_near = M.BAR / 2 + M.BOLT_SPREAD, M.BAR / 2 - M.BOLT_SPREAD
    k = Mb * 1000 / (d_far ** 2 + d_near ** 2)
    bolt = k * d_far
    # Arm bending at the pocket's edge, arm section 20 mm deep by the pocket width plus margins.
    t, w = M.BLOCK_HI - M.BLOCK_LO, M.BAR + 2 * M.MARGIN
    s_arm = Mb * 1000 / (w * t ** 2 / 6)
    name = "front (stops left turns)" if i == 0 else "rear (stops right turns)"
    print(f"{name}: bumper {r * 1000:.0f} mm from the axis, push {F:.0f} N")
    print(f"  bar root moment {Mb:.0f} N m over {lever:.0f} mm, bar stress {s_bar:.0f} MPa "
          f"(safety factor {AL_YIELD / s_bar:.1f} on yield)")
    print(f"  far bar bolt {bolt / 1000:.1f} kN (M6 8.8 proof 16.1 kN, factor {M6_PROOF / bolt:.1f})")
    print(f"  arm bending {s_arm:.0f} MPa (factor {AL_YIELD / s_arm:.1f})")

F_bolt = PINCH_TORQUE / (K_NUT * 0.006)                     # N per pinch bolt
F = 2 * F_bolt
r = S.HEAD_TUBE_R / 1000
T_slip = MU * np.pi * F * r
p = 2 * F / (2 * S.HEAD_TUBE_R * (M.BLOCK_HI - M.BLOCK_LO))
print(f"\nclamp: two M6 at {PINCH_TORQUE:.0f} N m, about {F_bolt / 1000:.1f} kN each")
print(f"  slip torque about {T_slip:.0f} N m (factor {T_slip / T:.1f} on the design load)")
print(f"  pressure on the head tube about {p:.0f} MPa; hoop stress {p * S.HEAD_TUBE_R / 2:.0f} MPa "
      f"for a 2 mm wall, {p * S.HEAD_TUBE_R / 3:.0f} MPa for 3 mm")
stem = MU * np.pi * 2 * (5.0 / (K_NUT * 0.005)) * 0.0143
print(f"  for scale, a stem clamp (two M5 at 5 N m on a 28.6 mm steerer) slips at about {stem:.0f} N m")
