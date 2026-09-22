# Morgan et al. (2017): Emissivity Measurements of Additively Manufactured Materials

**Source:** https://www.osti.gov/biblio/1341825 (LA-UR-17-20513)  
**Evidence boundary:** Full text read 2026-09-22 (OSTI PDF, 11 pp.). **VENUE FLAG: Los Alamos technical report, self-labelled "Preliminary Report" - NOT peer reviewed, no DOI, no stated uncertainty, no stated wavelength band.** Must be flagged as an unreviewed lab report wherever cited. **The only measured emissivity of printed PLA/ABS found.**

## Sensors

Gier-Dunkle reflectometer (normal emissivity from reflectivity, eps = 1 - r); FLIR SC8300 MWIR camera on a thermoelectric hot plate for the angular sweep.

### Pros

- Measures printed coupons (not raw resin), two build orientations each, duplicate samples.
- Candid about its own defects.

### Cons

- **No stated uncertainty, no wavelength band, no printer or process details.**
- The report **disowns its own angular-emissivity figure**: samples were still heating during the sweep, producing non-physical values.
- Colour is confounded with brand and material.

## Physical Box, Materials, and Geometry

Eight coupons 2 x 2 x 0.25 in, 0.2 mm layers, solid infill: Red ABS, uPrint ABS, conductive PLA, Gray PLA, Natural PLA. One printed vertically, one horizontally per material.

### Pros

- **Measured normal emissivity:** Red ABS 0.919/0.917; uPrint ABS 0.917/0.902; Gray PLA 0.916/0.923; Natural PLA 0.919/0.921; conductive PLA 0.883/0.897. Summary: "approximately 0.92" for all except conductive PLA.
- **Build orientation did not change emissivity** ("no observed change for most samples"); the one difference was within instrument error.
- Conductive (filled) PLA reads lower - a real caution that fillers reduce eps.
- Supports treating printed polymer walls as **high-emissivity**, unlike the low-eps metal shields this project contrasts itself against: this is the physical reason a printed shield re-radiates onto the sensor.

### Cons

- **No solar absorptance is measured anywhere.** The eps = alpha identity it quotes is the grey-body equilibrium relation, **not** a shortwave solar absorptance.

## Selection Lessons for This Project

- Cite **only** for measured normal IR emissivity of printed ABS/PLA (~0.88-0.92) and the null build-orientation result, **always flagged as an unreviewed LANL report (LA-UR-17-20513)**.
- Do **not** cite for solar absorptance, do **not** quote its angular curve (the authors disown it), and do **not** present eps = alpha as a solar-band claim.
