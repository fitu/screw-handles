# DIN 912 M4 press-on thumb cap

A rounded 28 × 12 mm wing handle for tool-free adjustment of a standard DIN 912 M4 socket-head screw. The cap pushes onto the exposed head, three small internal ribs retain it, and a hex peg engages the 3 mm socket.

## Download

- [Main STEP model](M4_DIN912_thumb_cap.step) — editable solid CAD, millimetres.
- [Main STL model](M4_DIN912_thumb_cap.stl) — ready to import into Bambu Studio.
- [Fit-test STEP](M4_fit_test.step) / [STL](M4_fit_test.stl) — smaller cap with the same fit geometry.
- [Printing notes and dimensions](PRINT_NOTES.txt).

Open a file on GitHub and click **Download raw file**, or use **Code → Download ZIP** for the whole package.

## Print and fit

Designed for PLA Basic on a Bambu H2D with a 0.4 mm nozzle. Print the flat exterior face down, with the pocket and peg pointing up. Suggested settings: 0.16 mm layers, 4 walls, 5 top/bottom layers, 30–40% infill, no supports.

The exported model includes a 0.2% linear shrinkage allowance. Cooled target dimensions include a 7.18 mm head pocket, three ribs at a 6.92 mm effective diameter (0.04 mm nominal radial interference on a 7.00 mm head), and a 2.94 mm AF hex peg with 1.8 mm insertion depth. Nominal exported envelope is approximately 28.06 × 12.02 × 7.62 mm, within a 30 mm diameter footprint.

Print the fit-test cap and let it cool before testing. Printer calibration and screw manufacturing tolerances affect retention. Fit and torque capacity have not been physically tested. Intended for light finger adjustment; no tightening torque rating is claimed.

## Source

`design.py` generates the STEP and STL files using CadQuery. With CadQuery installed, run `python design.py`; files are written to a `generated` folder beside the script. `validation.json` records the original solid-validity and STEP reimport checks.
