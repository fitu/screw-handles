# DIN 912 M4 nominal-dimension knurled cap

Round press-on cap with 40 straight knurl grooves and three drafted retention ribs. **All dimensions are nominal CAD millimetres. No shrinkage compensation is applied.**

![Exterior and pocket](preview.png)

## Files

- [Main STEP](M4_DIN912_thumb_cap.step) / [STL](M4_DIN912_thumb_cap.stl)
- [Fit-test STEP](M4_fit_test.step) / [STL](M4_fit_test.stl)
- [Printing and dimension notes](PRINT_NOTES.txt)

Use **Download raw file**, or **Code → Download ZIP** for the package.

## Current dimensions

| Feature | Nominal CAD value |
| --- | ---: |
| Outer diameter at knurl lands | 20.00 mm |
| Head bore diameter, away from ribs | 7.50 mm |
| Rib effective ID at pocket floor | 6.65 mm |
| Rib draft, towards wider opening | 3° |
| Rib height | 3.00 mm |
| Rib effective ID at free end | 6.96445 mm |
| Clear axial gap below chamfer | 0.20 mm |
| Hex drive across flats | 3.02 mm |
| Overall cap height | 7.60 mm |
| Pocket depth | 3.60 mm |
| Mouth chamfer | 0.40 × 45° |
| Mouth diameter | 8.30 mm |
| Hex insertion depth | 1.80 mm |

“Bottom” means the pocket floor, where the ribs attach. The floor is Z=4.00; the ribs end at Z=7.00. The mouth chamfer starts at Z=7.20 and reaches the lip at Z=7.60. The axial band Z=7.00–7.20 has the full Ø7.50 bore and no ribs.

Each rib is a rounded cone frustum. Its inner contact surface moves outward by `height × tan(3°)`, so effective rib ID increases from 6.65 to 6.96445 mm towards the opening. The three ribs are spaced 120° apart. The hex has a 3.02 mm AF driving section followed by a 0.30 mm tapered tip to 2.53 mm AF.

## Printing

Bambu H2D / PLA Basic, 0.4 mm nozzle: suggested 0.16 mm layers, 4 walls, 5 top/bottom layers, 30–40% infill. Flat outer face down, pocket and hex peg up; no supports. Print at 100% for these nominal dimensions. The previous 1.6% compensation and previous rib acceptance limits are superseded.

Print the updated fit-test cap first. Actual printed fit depends on material and printer calibration. The requested 3.02 mm hex has little clearance in a socket at its minimum size; check alignment and fit before pressing. For light finger adjustment; no physical fit or torque testing has been performed.

## Source and validation

`python design.py` (requires CadQuery) exports the models into a `generated` folder beside the script. No scaling is applied. Both STEP files are reimported and checked as single valid solids. Checks measure three rib sections, the clear band below the chamfer, and the 3.02 mm hex AF directly from the STEP geometry. Results are in [validation.json](validation.json).
