"""Nominal CAD dimensions in mm. No shrinkage compensation."""
import cadquery as cq
import math, json
from pathlib import Path
OUT=Path(__file__).resolve().parent/'generated'
OUT.mkdir(parents=True,exist_ok=True)
OD=20.0
ID=7.5
HEIGHT=7.6
FLOOR=4.0
CHAMFER_HEIGHT=.4
CHAMFER_START=HEIGHT-CHAMFER_HEIGHT
RIB_TOP_GAP=.2
RIB_END=CHAMFER_START-RIB_TOP_GAP
RIB_BOTTOM_ID=6.65
RIB_DRAFT_DEG=3.0
RIB_RADIUS=.38
RIB_HEIGHT=RIB_END-FLOOR
RIB_TOP_RADIUS=RIB_RADIUS-RIB_HEIGHT*math.tan(math.radians(RIB_DRAFT_DEG))
RIB_TOP_ID=RIB_BOTTOM_ID+2*RIB_HEIGHT*math.tan(math.radians(RIB_DRAFT_DEG))
HEX_AF=3.02

def hexpts(af):
 r=af/math.sqrt(3)
 return [(r*math.cos(i*math.pi/3),r*math.sin(i*math.pi/3)) for i in range(6)]

def cap(knurled=True):
 radius=OD/2 if knurled else 5.5
 body=cq.Workplane('XY').circle(radius).extrude(HEIGHT)
 if knurled:
  body=body.edges('>Z or <Z').fillet(.5)
  centers=[((radius-.05)*math.cos(2*math.pi*i/40),
            (radius-.05)*math.sin(2*math.pi*i/40)) for i in range(40)]
  cutters=cq.Workplane('XY').workplane(offset=-.1).pushPoints(centers).circle(.45).extrude(HEIGHT+.2)
  body=body.cut(cutters)
 pocket=cq.Workplane('XY').workplane(offset=FLOOR).circle(ID/2).extrude(HEIGHT-FLOOR+.1)
 body=body.cut(pocket)
 lead=cq.Solid.makeCone(ID/2,ID/2+CHAMFER_HEIGHT,CHAMFER_HEIGHT,cq.Vector(0,0,CHAMFER_START))
 body=body.cut(lead)
 # Three conical ribs: inward contact surface drafts 3 degrees away from axis
 # towards the opening; the rib stops 0.2 mm below the chamfer start.
 rc=RIB_BOTTOM_ID/2+RIB_RADIUS
 for a in [0,120,240]:
  x,y=rc*math.cos(math.radians(a)),rc*math.sin(math.radians(a))
  rib=cq.Solid.makeCone(RIB_RADIUS,RIB_TOP_RADIUS,RIB_HEIGHT,cq.Vector(x,y,FLOOR))
  body=body.union(rib)
 peg=cq.Workplane('XY').workplane(offset=FLOOR-.05).polyline(hexpts(HEX_AF)).close().extrude(1.55)
 tip=(cq.Workplane('XY').workplane(offset=FLOOR+1.5).polyline(hexpts(HEX_AF)).close()
      .workplane(offset=.3).polyline(hexpts(HEX_AF-.49)).close().loft())
 return body.union(peg).union(tip).clean().val()

def ray_radii(shape,z,angle):
 u=(math.cos(math.radians(angle)),math.sin(math.radians(angle)))
 ray=cq.Edge.makeLine(cq.Vector(0,0,z),cq.Vector(12*u[0],12*u[1],z))
 return sorted(v.X*u[0]+v.Y*u[1] for v in shape.intersect(ray).Vertices())

results={'units':'mm','shrinkage_compensation':False,'CAD_scale_factor':1.0,
 'nominal_OD_mm':OD,'nominal_bore_ID_mm':ID,'height_mm':HEIGHT,
 'pocket_floor_z_mm':FLOOR,'chamfer_start_z_mm':CHAMFER_START,
 'rib_bottom_ID_mm':RIB_BOTTOM_ID,'rib_draft_degrees':RIB_DRAFT_DEG,
 'rib_end_z_mm':RIB_END,'rib_to_chamfer_gap_mm':RIB_TOP_GAP,
 'rib_top_ID_mm':RIB_TOP_ID,'hex_AF_mm':HEX_AF,'knurl_grooves':40}
assert RIB_TOP_RADIUS>0
for name,knurled in [('M4_DIN912_thumb_cap',True),('M4_fit_test',False)]:
 shape=cap(knurled)
 assert shape.isValid() and len(shape.Solids())==1
 cq.exporters.export(shape,str(OUT/(name+'.step')))
 cq.exporters.export(shape,str(OUT/(name+'.stl')),tolerance=.01,angularTolerance=.1)
 reread=cq.importers.importStep(str(OUT/(name+'.step'))).val()
 assert reread.isValid() and len(reread.Solids())==1
 samples=[]
 for z in [FLOOR+.001,5.5,RIB_END-.001]:
  expected=RIB_BOTTOM_ID+2*(z-FLOOR)*math.tan(math.radians(RIB_DRAFT_DEG))
  ids=[2*min(r for r in ray_radii(reread,z,a) if r>2) for a in [0,120,240]]
  assert all(abs(d-expected)<1e-5 for d in ids),(z,ids,expected)
  samples.append({'z_mm':z,'measured_rib_IDs_mm':ids})
 # Check the entire requested clear band at its midpoint has the full bore ID.
 ids=[2*min(r for r in ray_radii(reread,RIB_END+.1,a) if r>2) for a in [0,120,240]]
 assert all(abs(d-ID)<1e-5 for d in ids),ids
 # At 90 degrees, hex has a flat face at AF/2.
 hex_af=2*min(r for r in ray_radii(reread,4.5,90) if r>.1)
 assert abs(hex_af-HEX_AF)<1e-5,hex_af
 b=shape.BoundingBox()
 results[name]={'size_mm':[b.xlen,b.ylen,b.zlen],'volume_mm3':shape.Volume(),
  'valid_STEP_roundtrip':True,'solid_count':1,'rib_sections':samples,
  'clear_band_bore_IDs_mm':ids,'measured_hex_AF_mm':hex_af}
(OUT/'validation.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
