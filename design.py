import cadquery as cq, math, json
from pathlib import Path
out=Path(__file__).resolve().parent / 'generated'
out.mkdir(parents=True, exist_ok=True)
SHRINKAGE = 0.016  # User-specified linear shrinkage, 1.6%
S = 1 / (1 - SHRINKAGE)
HEAD_MIN = 6.78
HEAD_MAX_PLAIN = 7.00
HEAD_MAX_KNURLED = 7.22
MIN_INTERFERENCE = 0.02  # Diametral, finished part requirement.
RIB_ACCEPT_MAX = HEAD_MIN - MIN_INTERFERENCE  # 6.76 mm
RIB_TARGET = 6.74  # 0.02 mm diametral allowance below acceptance maximum.
POCKET_DIA = 7.40  # Clears the largest permitted knurled screw head.
# All design dimensions below are desired cooled dimensions; scale at export.
def hexpts(af):
 r=af/math.sqrt(3)
 return [(r*math.cos(i*math.pi/3),r*math.sin(i*math.pi/3)) for i in range(6)]
def cap(knurled=True, rib_id=RIB_TARGET):
 if knurled:
  # 15 mm cooled maximum diameter, with 30 support-free axial grip grooves.
  body=cq.Workplane('XY').circle(7.5).extrude(7.6)
  body=body.edges('>Z or <Z').fillet(.5)
  centers=[(7.45*math.cos(2*math.pi*i/30),
            7.45*math.sin(2*math.pi*i/30)) for i in range(30)]
  cutters=(cq.Workplane('XY').workplane(offset=-.1)
           .pushPoints(centers).circle(.45).extrude(7.8))
  body=body.cut(cutters)
 else:
  body=cq.Workplane('XY').circle(5.5).extrude(7.6)
 # head-side pocket: roof at 4, lip at 7.6; leaves screw underside 0.4 proud
 pocket=cq.Workplane('XY').workplane(offset=4).circle(POCKET_DIA/2).extrude(4)
 body=body.cut(pocket)
 # 0.4 x 45 degree lead-in at cavity mouth
 lead=cq.Solid.makeCone(POCKET_DIA/2,POCKET_DIA/2+.4,.4,cq.Vector(0,0,7.2))
 body=body.cut(lead)
 # Three rounded crush ribs; 0.04 mm target diametral interference at head minimum.
 # Individual tapered entries reduce the insertion step on larger heads.
 rr=.38; rc=rib_id/2+rr
 for a in [0,120,240]:
  x,y=rc*math.cos(math.radians(a)),rc*math.sin(math.radians(a))
  rib=cq.Workplane('XY').workplane(offset=4).center(x,y).circle(rr).extrude(2.8)
  ramp=cq.Solid.makeCone(rr,0,.4,cq.Vector(x,y,6.8))
  body=body.union(rib).union(ramp)
 body=body.cut(lead)
 # Small hex drive, slight clearance; 1.8 insertion avoids socket bottoming.
 peg=(cq.Workplane('XY').workplane(offset=3.95).polyline(hexpts(2.94)).close().extrude(1.55))
 tip=(cq.Workplane('XY').workplane(offset=5.5).polyline(hexpts(2.94)).close().workplane(offset=.3).polyline(hexpts(2.45)).close().loft())
 return body.union(peg).union(tip).clean().val().scale(S)
results={'linear_shrinkage': SHRINKAGE, 'CAD_scale_factor': S,
         'cooled_target_OD_mm':15.0, 'knurl_grooves':30,
         'cooled_rib_effective_ID_mm':RIB_TARGET,
         'finished_rib_effective_ID_max_mm':RIB_ACCEPT_MAX,
         'cooled_head_pocket_ID_mm':POCKET_DIA,
         'head_OD_min_mm':HEAD_MIN,
         'head_OD_max_plain_mm':HEAD_MAX_PLAIN,
         'head_OD_max_knurled_mm':HEAD_MAX_KNURLED,
         'minimum_required_diametral_interference_mm':MIN_INTERFERENCE,
         'minimum_target_diametral_interference_mm':round(HEAD_MIN-RIB_TARGET,6),
         'target_interference_at_plain_max_mm':round(HEAD_MAX_PLAIN-RIB_TARGET,6),
         'target_interference_at_knurled_max_mm':round(HEAD_MAX_KNURLED-RIB_TARGET,6),
         'cap_positive_diameter_allowance_mm':round(RIB_ACCEPT_MAX-RIB_TARGET,6),
         'physical_fit_verified':False}
assert HEAD_MIN - RIB_ACCEPT_MAX >= MIN_INTERFERENCE - 1e-9
assert RIB_TARGET <= RIB_ACCEPT_MAX
assert POCKET_DIA > HEAD_MAX_KNURLED
for name,knurled in [('M4_DIN912_thumb_cap',True),('M4_fit_test',False)]:
 shape=cap(knurled)
 assert shape.isValid() and len(shape.Solids())==1
 cq.exporters.export(shape,str(out/(name+'.step')))
 cq.exporters.export(shape,str(out/(name+'.stl')),tolerance=.015,angularTolerance=.1)
 reread=cq.importers.importStep(str(out/(name+'.step'))).val()
 assert reread.isValid() and len(reread.Solids())==1
 b=shape.BoundingBox()
 results[name]={'size_mm':[b.xlen,b.ylen,b.zlen],'volume_mm3':shape.Volume(),'valid_STEP_roundtrip':True, 'solid_count':len(shape.Solids())}
(out/'validation.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
