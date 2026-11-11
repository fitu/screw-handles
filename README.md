# DIN 912 M4 knurled press-on screw cap

A **15 mm cooled target diameter** knob with 30 straight knurl grooves. Three internal ribs retain the cap on the screw head; a hex peg engages the 3 mm socket for tool-free adjustment. The ribs are now sized against the minimum permitted head diameter.

![Knurled cap exterior and head pocket](preview.png)

## Download

- [Main STEP model](M4_DIN912_thumb_cap.step) — solid CAD in millimetres.
- [Main STL model](M4_DIN912_thumb_cap.stl) — import into Bambu Studio.
- [Fit-test STEP](M4_fit_test.step) / [STL](M4_fit_test.stl) — smaller cap with the same pocket, ribs and peg.
- [Printing notes](PRINT_NOTES.txt).

Open a file and select **Download raw file**, or use **Code → Download ZIP** for the package.

## Head tolerance and rib fit

The M4 head diameter is **6.78–7.00 mm for a smooth head**, per [Böllhoff's DIN 912 data sheet](https://eshop.boellhoff.de/out/media/pdf/DIN_912_Stahl_10.9___en.pdf). The [H.J DIN 912 manufacturer table](https://www.hjfasteners.com/userfiles/Fl202205302235287842.pdf) gives a **7.22 mm maximum for a knurled screw head**, with the same 6.78 mm minimum.

The cooled effective rib diameter is **6.74 mm**. Its finished acceptance maximum is **6.76 mm**, leaving 0.02 mm of upward process allowance. At that acceptance limit, a minimum-size 6.78 mm head still has **0.02 mm diametral interference**. The CAD target gives 0.04 mm interference on that head.

| Screw head diameter | Interference at 6.74 mm design target | Interference at 6.76 mm acceptance maximum |
| --- | ---: | ---: |
| 6.78 mm — minimum head | 0.04 mm diametral | 0.02 mm diametral |
| 7.00 mm — smooth-head maximum / nominal | 0.26 mm diametral | 0.24 mm diametral |
| 7.22 mm — knurled-head maximum | 0.48 mm diametral | 0.46 mm diametral |

Radial interference is half these values. The larger heads require more rib displacement; insertion force and durability have not been measured. The pocket is enlarged to a **7.40 mm cooled target** to clear the maximum knurled head away from the ribs. Each rib has a tapered entry ramp.

The 0.02 mm minimum applies to accepted finished geometry, not an unmeasured print. Check the cooled effective opening is no larger than 6.76 mm; printer error and shrinkage variation must fit within the 0.02 mm upward allowance. The supplied fit-test cap uses the same updated ribs.

## Dimensions and shrinkage

All exported geometry includes **1.6% uniform linear PLA shrinkage compensation**: `CAD dimension = cooled target / 0.984`.

| Feature | Cooled target | Compensated CAD dimension |
| --- | ---: | ---: |
| Maximum knob diameter | 15.000 mm | 15.244 mm |
| Overall height | 7.600 mm | 7.724 mm |
| Head pocket diameter | 7.400 mm | 7.520 mm |
| Head pocket depth | 3.600 mm | 3.659 mm |
| Pocket entry diameter | 8.200 mm | 8.333 mm |
| Effective rib diameter | 6.740 mm | 6.850 mm |
| Hex peg across flats | 2.940 mm | 2.988 mm |
| Hex insertion depth | 1.800 mm | 1.829 mm |

The grip has 30 axial grooves made with 0.90 mm diameter cutters at radius 7.45 mm before compensation. Ribs have a rounded 0.38 mm cross-section radius, a 2.8 mm constant section and a 0.4 mm conical entry ramp. The rim surrounds the upper 3.6 mm of the head, leaving at least 0.22 mm nominal mounting-surface clearance for a 3.82 mm minimum-height head.

## Bambu H2D / PLA Basic

Use a 0.4 mm nozzle, calibrated PLA Basic profile, 0.16 mm layers, 4 walls, 5 top/bottom layers and 30–40% infill. Put the flat exterior face on the bed, with the pocket and peg up. No supports required.

**Print at 100% scale. Do not add another shrinkage compensation in Bambu Studio or the filament profile.** The files include the full 1.6% allowance. Print the fit-test cap first and let it cool fully. Verify fit and the effective rib opening before printing the knob. This geometry has not been physically validated and has no rated insertion force or tightening torque. Intended for light finger adjustment.

## Source and validation

With CadQuery installed, run `python design.py`; models are written to a `generated` folder beside the script. STEP exports are checked as single valid solids and reimported. See [validation.json](validation.json).
