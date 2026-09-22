# Formetta et al. (2016): Performance of Site-Specific Longwave Radiation Parameterizations

**Source:** https://doi.org/10.5194/hess-20-4641-2016  
**Evidence boundary:** Full text read 2026-09-22 (open-access version of record). Archival journal. **Independent multi-site validation bounding how good any clear-sky sky-temperature model can be.**

## Sensors

**Eppley pyrgeometers, +/-3 W/m^2**, at 24 AmeriFlux stations across the contiguous USA; station air temperature, RH, soil temperature, precipitation and incoming solar for the clearness index. Hourly data from Level-2 30-min averages.

### Pros

- Independent, multi-site, multi-year validation **with a stated reference-instrument uncertainty**, so a defensible error bar can be quoted on the radiative sky term.
- Prints the Swinbank, Brunt, Idso, Brutsaert and Konzelmann forms with coefficients in one verified table - so this project can reference Swinbank's equation correctly without citing a paper it has not read.

### Cons

- Sites are continental-US flux towers over vegetated surfaces; none is a rooftop, street or instrument-enclosure siting.
- Reports RMSE in **W/m^2 of flux, not in K of sky temperature** - conversion is the reader's job and depends on T_air.
- Says nothing about enclosures, surfaces or view factors; a real enclosure sees ground as well as sky.

## Physical Box, Materials, and Geometry

Not applicable.

### Pros

- Benchmarks 10 clear-sky parameterizations: with literature coefficients, **Idso (1981) and Brunt (1932) perform best (mean KGE 0.75-0.92, RMSE max 39 W/m^2)**; Konzelmann is worst because its parameters were fitted in Greenland.
- **Quantifies the transferability penalty directly:** site-specific recalibration roughly **halves** the RMSE at every site.

### Cons

- **Does not support a single hard-coded offset:** even the best physically-parameterized models carry tens of W/m^2 of RMSE with literature coefficients, and coefficients are demonstrably site-specific. A fixed 20 K carries strictly less information than any of them.

## Selection Lessons for This Project

- Cite for: RMSE/KGE bounds on clear-sky longwave parameterizations, the verified functional forms, and the evidence that coefficients are site-specific (hence sky temperature is a calibrated input, not a constant).
- Do **not** cite it for a sky-temperature depression in kelvin, for enclosure or urban siting, or for sky view factor.
