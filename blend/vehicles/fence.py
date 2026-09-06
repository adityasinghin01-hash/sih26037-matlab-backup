"""fence.py - THE S2 POST-AND-RAIL FENCE, BLENDER-AUTHORED.

SPEC.md calls this fence out explicitly as "massed, not detailed" - a
deliberate choice, not an oversight, and it repeats about 114 times around
the gyratory (measured: S2's own render log). A heavily detailed multi-part
fence at that instance count would work against both that written intent and
against render speed, which has been the priority all session. So this stays
modest: real Blender geometry (an octagonal post with a chamfered top instead
of a sharp cuboid, a rail with slightly rounded long edges instead of a bare
box), not a from-scratch redesign - genuinely better than sc.box3's flat
rectangular prisms, without adding real cost at 114x repetition.

TWO PARTS, UNIT-SIZED for per-instance scaling in MATLAB exactly like every
other instanced prop in this project (trees, grass, scrub):
  fence_post  - real absolute size (0.10 x 0.10 x 1.05 m), posts never resize
  fence_rail  - unit length (1 m) along x, real cross-section, scaled by
                span length per instance the same way sc.roadTexture's own
                caller already varies length per call
"""
import bpy, math, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from _veh import reset, obj_from, export

reset()

# ---------------------------------------------------------------- the post
# Octagonal, not square - the one upgrade that matters here, since posts
# stand upright against the sky/treeline and a sharp square edge is the most
# visible "cuboid" tell in the current fence. A small chamfered top (two
# rings, the top pulled in) sheds the flat-topped-stick look real posts don't
# have, for the cost of 8 extra vertices - nothing at 114 instances.
R, H = 0.055, 1.05
CHAMFER_H, CHAMFER_R = 0.05, 0.030
n = 8
v = []
for zz, rr in [(0.0, R), (H - CHAMFER_H, R), (H, CHAMFER_R)]:
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
f.append(tuple(range(n - 1, -1, -1)))          # bottom cap
f.append(tuple(range(2 * n, 3 * n)))           # top cap (chamfered, not flush)
post = obj_from("fence_post", v, f)

# ---------------------------------------------------------------- the rail
# Unit length along x, real 0.05 x 0.09 cross-section, MATLAB scales x per
# span. Long edges chamfered (an octagonal cross-section stretched, not a
# cuboid) - cheap, and it is what stops a rail reading as a plank.
RW, RD = 0.05, 0.09
v2, f2 = [], []
prof = [(-RW/2, -RD/2*0.7), (-RW/2*0.7, -RD/2), (RW/2*0.7, -RD/2),
        (RW/2, -RD/2*0.7),  (RW/2, RD/2*0.7),   (RW/2*0.7, RD/2),
        (-RW/2*0.7, RD/2),  (-RW/2, RD/2*0.7)]
m = len(prof)
for xx in (-0.5, 0.5):
    for (py, pz) in prof:
        v2.append((xx, py, pz))
for i in range(m):
    j = (i + 1) % m
    f2.append((i, j, m + j, m + i))
f2.append(tuple(range(m - 1, -1, -1)))
f2.append(tuple(range(m, 2 * m)))
rail = obj_from("fence_rail", v2, f2)

out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "matlab", "assets")
tris = export(["fence_post", "fence_rail"], out_dir)
print("FENCE total tris:", tris)
