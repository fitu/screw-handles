import cadquery as cq, math, json
from pathlib import Path
out=Path(__file__).resolve().parent / 'generated'
out.mkdir(parents=True, exist_ok=True)
SHRINKAGE = 0.016  # User-specified linear shrinkage, 1.6%
S = 1 / (1 - SHRINKAGE)
# All design dimensions below are desired cooled dimensions; scale at export.
def hexpts(af):
 r=af/math.sqrt(3)
 return [(r*math.cos(i*math.pi/3),r*math.sin(i*math.pi/3)) for i in range(6)]
def cap(knurled=True, rib_id=6.88):
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
 pocket=cq.Workplane('XY').workplane(offset=4).circle(3.59).extrude(4)
 body=body.cut(pocket)
 # 0.4 x 45 degree lead-in at cavity mouth
 lead=cq.Solid.makeCone(3.59,3.99,.4,cq.Vector(0,0,7.2))
 body=body.cut(lead)
 # Three rounded, locally yielding ribs. 0.12 mm diametral / 0.06 mm radial interference on nominal head.
 rr=.38; rc=rib_id/2+rr
 for a in [0,120,240]:
  x,y=rc*math.cos(math.radians(a)),rc*math.sin(math.radians(a))
  rib=cq.Workplane('XY').workplane(offset=4).center(x,y).circle(rr).extrude(3.2)
  body=body.union(rib)
 body=body.cut(lead)
 # Small hex drive, slight clearance; 1.8 insertion avoids socket bottoming.
 peg=(cq.Workplane('XY').workplane(offset=3.95).polyline(hexpts(2.94)).close().extrude(1.55))
 tip=(cq.Workplane('XY').workplane(offset=5.5).polyline(hexpts(2.94)).close().workplane(offset=.3).polyline(hexpts(2.45)).close().loft())
 return body.union(peg).union(tip).clean().val().scale(S)
results={'linear_shrinkage': SHRINKAGE, 'CAD_scale_factor': S,
         'cooled_target_OD_mm':15.0, 'knurl_grooves':30,
         'cooled_rib_effective_ID_mm':6.88,
         'nominal_head_OD_mm':7.0, 'cooled_diametral_interference_mm':0.12}
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
