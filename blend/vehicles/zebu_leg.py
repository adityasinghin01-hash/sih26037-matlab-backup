"""zebu_leg.py - ONE new moving leg part for the zebu, per the same principle
this project already used seven times for burial: nothing is cut from the
downloaded zebu.stl (rigging or slicing an unfamiliar organic mesh blind, with
no way to preview the result before it ships, is exactly the kind of thing
this project's own traps warn against). Instead, a slightly LARGER leg is
drawn OVER the same position and made to swing - "step outward", the same
fix that solved the car's wheel/rim/hub - so it occludes the original static
leg underneath rather than requiring it to be removed.

Measured off the actual zebu.stl in MATLAB, not guessed: all four legs
attach at the SAME height (z=0.657 m from the ground, in the model's own
1.46 m tall frame), front pair near x=+0.234, rear pair near x=-0.713 (+x
confirmed as FRONT by cross-referencing sc.zebuColours' own muzzle test,
which is only true at high +x).

Built UNIT-HEIGHT (top at z=1, base at z=0) tapered cylinder, forward-facing
end down, so MATLAB scales it by the real 0.657 m pivot-to-hoof length and
rotates it about its own TOP (z=1) for the fore-aft gait swing - a rotation
sc.scene's instances()/mesh() cannot do (Yaw is Z-axis only), so the actual
per-frame rotation is computed directly on this mesh's vertices in MATLAB,
not through the standard instancing path.
"""
import bpy, math, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from _veh import reset, obj_from, export

reset()

# Slightly chunkier than a real leg on purpose - "step outward" needs it
# provably wider than whatever silhouette the original mesh's own leg has,
# not a best-guess match to it.
n = 8
R_TOP, R_BOT = 0.062, 0.046
v = []
for zz, rr in [(1.0, R_TOP), (0.08, R_BOT * 1.05), (0.0, R_BOT)]:
    for i in range(n):
        a = 2 * math.pi * i / n
        v.append((rr * math.cos(a), rr * math.sin(a), zz))
f = []
for ring in range(2):
    for i in range(n):
        j = (i + 1) % n
        a, b = ring * n + i, ring * n + j
        c, d = (ring + 1) * n + j, (ring + 1) * n + i
        f.append((a, b, c, d))
f.append(tuple(range(n - 1, -1, -1)))          # top cap (at the hip pivot)
f.append(tuple(range(2 * n, 3 * n)))           # bottom cap (the hoof)
leg = obj_from("zebu_leg", v, f)

out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "matlab", "assets")
tris = export(["zebu_leg"], out_dir)
print("ZEBU LEG tris:", tris)
