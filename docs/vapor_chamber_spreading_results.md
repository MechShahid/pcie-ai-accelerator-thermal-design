\# Vapor-Chamber / Spreading-Resistance Results



\## Purpose



This study adds the missing chip-to-base spreading resistance to the previous forced-air heatsink model.



The earlier forced-air model mainly evaluated the air-side heat rejection capability of the fin stack. It did not explicitly resolve the three-dimensional spreading resistance caused by transferring heat from a 45 mm × 45 mm chip into a larger heatsink base.



This result document answers the following engineering question:



```text

Does reducing spreading resistance using copper or a vapor chamber meaningfully reduce chip temperature, or is the design still dominated by air-side resistance?

```



\## Thermal Resistance Network



The chip-to-air resistance network is:



```text

R\_total = R\_TIM + R\_base,1D + R\_spreading + R\_air

```



where:



| Term | Meaning |

|---|---|

| `R\_TIM` | bulk thermal interface material resistance |

| `R\_base,1D` | one-dimensional through-thickness base conduction resistance |

| `R\_spreading` | excess spreading resistance from chip footprint to larger base |

| `R\_air` | forced-air fin-stack resistance from the previous heat-exchanger model |



The chip temperature is calculated as:



```text

T\_chip = T\_air,in + Q\_chip × R\_total

```



with:



| Parameter | Value |

|---|---:|

| Chip heat load | 250 W |

| Inlet air temperature | 25 °C |

| Target chip temperature | 85 °C |

| Chip/source area | 45 mm × 45 mm |

| TIM resistance | 0.0165 K/W |



\## Cases Compared



Two forced-air heatsink cases were evaluated.



| Case | Geometry / condition | Purpose |

|---|---|---|

| Compact baseline | 80 × 80 × 25 mm at 4 m/s | Check whether vapor chamber can rescue the compact design |

| Recommended candidate | 80 × 100 × 50 mm at 5 m/s | Check whether vapor chamber improves margin for a passing forced-air design |



For each forced-air case, the following base/spreader architectures were compared:



| Architecture | Model |

|---|---|

| Aluminum 6061 base | isotropic solid conduction |

| Aluminum high-k base | isotropic solid conduction |

| Copper spreader | isotropic solid conduction |

| Vapor chamber conservative | equivalent anisotropic heat spreader |

| Vapor chamber baseline | equivalent anisotropic heat spreader |

| Vapor chamber optimistic sensitivity | equivalent anisotropic heat spreader |



The vapor chamber was not modelled as a detailed two-phase device. It was represented as an equivalent anisotropic heat spreader to capture its main role: lateral heat spreading.



\## Compact Baseline Result



The compact baseline case is:



```text

80 × 80 × 25 mm heatsink

channel velocity = 4 m/s

```



The results are:



| Architecture | R\_spreading (K/W) | R\_air (K/W) | T\_chip (°C) | Status |

|---|---:|---:|---:|---|

| Aluminum 6061 | 0.0063 | 0.3975 | 131.3 | FAIL |

| Aluminum high-k | 0.0053 | 0.3975 | 130.8 | FAIL |

| Copper spreader | 0.0028 | 0.3975 | 129.7 | FAIL |

| Vapor chamber conservative | 0.0009 | 0.3975 | 130.0 | FAIL |

| Vapor chamber baseline | 0.0006 | 0.3975 | 129.3 | FAIL |

| Vapor chamber optimistic | 0.0002 | 0.3975 | 129.0 | FAIL |



\### Interpretation



The compact baseline fails badly for every base/spreader architecture.



Even the optimistic vapor chamber case gives:



```text

T\_chip = 129.0 °C

Target = 85.0 °C

Margin = -44.0 °C

```



The resistance split shows why:



```text

R\_air = 0.3975 K/W

R\_spreading = 0.0002–0.0063 K/W

```



The air-side resistance is much larger than the spreading resistance.



Therefore, the compact baseline is air-side dominated.



A vapor chamber cannot rescue the compact 80 × 80 × 25 mm forced-air heatsink because the dominant limitation is air-side heat rejection, not chip-to-base spreading.



\## Recommended Forced-Air Candidate Result



The recommended forced-air candidate is:



```text

80 × 100 × 50 mm heatsink

channel velocity = 5 m/s

```



The results are:



| Architecture | R\_spreading (K/W) | R\_air (K/W) | T\_chip (°C) | Margin (°C) | Status |

|---|---:|---:|---:|---:|---|

| Aluminum 6061 | 0.0072 | 0.2023 | 82.4 | 2.6 | PASS |

| Aluminum high-k | 0.0061 | 0.2023 | 82.0 | 3.0 | PASS |

| Copper spreader | 0.0033 | 0.2023 | 80.9 | 4.1 | PASS |

| Vapor chamber conservative | 0.0010 | 0.2023 | 81.0 | 4.0 | PASS |

| Vapor chamber baseline | 0.0007 | 0.2023 | 80.4 | 4.6 | PASS |

| Vapor chamber optimistic | 0.0003 | 0.2023 | 80.2 | 4.8 | PASS |



\### Interpretation



The recommended forced-air candidate already passes with an aluminum base:



```text

Aluminum 6061:

T\_chip = 82.4 °C

Margin = 2.6 °C

```



A copper spreader improves the predicted chip temperature to:



```text

Copper:

T\_chip = 80.9 °C

Margin = 4.1 °C

```



The vapor chamber baseline improves the predicted chip temperature to:



```text

Vapor chamber baseline:

T\_chip = 80.4 °C

Margin = 4.6 °C

```



Compared with aluminum 6061, the vapor chamber baseline improves chip temperature by approximately:



```text

82.4 - 80.4 = 2.0 °C

```



Therefore, for this geometry, the vapor chamber improves thermal margin, but the improvement is modest.



\## Main Engineering Conclusion



Reducing spreading resistance improves chip temperature, but only modestly for the geometries studied.



The dominant resistance remains the air-side fin-stack resistance.



This is shown by the resistance split:



```text

Compact baseline:

R\_air ≈ 0.3975 K/W

R\_spreading ≈ 0.0002–0.0063 K/W



Recommended forced-air candidate:

R\_air ≈ 0.2023 K/W

R\_spreading ≈ 0.0003–0.0072 K/W

```



In both cases, air-side resistance is much larger than spreading resistance.



Therefore:



```text

The first design priority is sufficient airflow and fin area.

A vapor chamber is useful mainly for hotspot reduction and thermal-margin improvement.

It is not a substitute for adequate air-side heat rejection.

```



\## Design Implication



| Design option | Result |

|---|---|

| Compact aluminum heatsink | Fails badly |

| Compact copper spreader | Still fails badly |

| Compact vapor chamber | Still fails badly |

| Larger forced-air aluminum heatsink | Passes with small margin |

| Larger forced-air copper spreader | Passes with improved margin |

| Larger forced-air vapor chamber | Passes with slightly improved margin |



The vapor chamber should only be carried forward if the design objective includes hotspot reduction, improved thermal margin, or improved temperature uniformity.



For bulk heat rejection, airflow and fin area remain the controlling design parameters.



\## Model Limitation



The spreading-resistance values are based on an equivalent circular analytical approximation.



The actual chip and base geometries are rectangular:



```text

chip = 45 mm × 45 mm

base = 80 mm × 80 mm or 80 mm × 100 mm

```



The equivalent circular method is used only for architecture-level screening.



Final CFD/FEA should resolve the true rectangular geometry and local temperature field.



\## Recommended Next Verification



Before final reporting, include a simple verification check:



```text

When A\_source = A\_base, R\_spreading should approach zero.

```



This confirms that the spreading-resistance implementation behaves correctly in the no-spreading limit.

