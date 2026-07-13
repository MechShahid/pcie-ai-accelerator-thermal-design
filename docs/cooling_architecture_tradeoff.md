\# Cooling Architecture Tradeoff Summary



\## Purpose



This document summarizes the cooling architecture decisions for the 250 W PCIe AI accelerator thermal design study.



The goal is to compare passive cooling, compact forced-air cooling, larger forced-air cooling, and vapor-chamber-assisted spreading before moving to CAD/CFD.



This step is important because the project should not blindly jump to CFD. The analytical screening identifies which cooling architecture is physically reasonable and which design variables control the result.



\## Design Target



| Parameter | Value |

|---|---:|

| Chip heat load | 250 W |

| Inlet / ambient air temperature | 25 °C |

| Target chip temperature | 85 °C |

| Required chip-to-air resistance | 0.240 K/W |

| Chip size | 45 mm × 45 mm |

| TIM baseline | 0.2 mm, 6 W/mK |

| TIM resistance | approximately 0.0165 K/W |



The required chip-to-air thermal resistance is:



```text

R\_required = (85 - 25) / 250 = 0.240 K/W

```



Any cooling architecture must keep the total resistance below this value.



\## Architecture 1: Passive / Fanless Cooling



Passive cooling was evaluated using natural convection and radiation.



The model included:



| Surface group | Model |

|---|---|

| Fin-channel walls | Elenbaas-type natural convection + Shabany channel radiation |

| Exposed fin tips and outer faces | natural convection + gray-body radiation |

| Bottom chip-contact surface | excluded from convection/radiation |



Two geometries were evaluated:



| Geometry | Size |

|---|---|

| Compact baseline | 80 × 80 × 25 mm |

| Larger candidate | 80 × 100 × 50 mm |



At 85 °C heatsink surface temperature and black-anodized emissivity, the best passive heat rejection was:



| Geometry | Surrounding temperature | Passive heat rejection |

|---|---:|---:|

| Compact 80 × 80 × 25 mm | 25 °C | 25.1 W |

| Larger 80 × 100 × 50 mm | 25 °C | 37.9 W |



The required heat rejection is 250 W.



Therefore:



```text

Best passive case = 37.9 W

Required = 250 W

Fraction removed = 37.9 / 250 ≈ 15 %

```



\### Passive Cooling Conclusion



Passive/fanless cooling is not feasible for the 250 W chip case.



Even with optimistic black-anodized radiation and open ambient surroundings, passive cooling removes only a small fraction of the required heat load.



The passive architecture is therefore excluded from the main design path.



\## Architecture 2: Compact Forced-Air Heatsink



The compact forced-air heatsink case was:



```text

80 × 80 × 25 mm heatsink

channel velocity = 4 m/s

```



The previous forced-air heat-exchanger model predicted that this compact case fails the 85 °C target.



After adding TIM, base conduction, and spreading resistance, the compact result remained far above the target.



| Base / spreader | T\_chip | Status |

|---|---:|---|

| Aluminum 6061 | 131.3 °C | FAIL |

| Aluminum high-k | 130.8 °C | FAIL |

| Copper spreader | 129.7 °C | FAIL |

| Vapor chamber conservative | 130.0 °C | FAIL |

| Vapor chamber baseline | 129.3 °C | FAIL |

| Vapor chamber optimistic | 129.0 °C | FAIL |



The best compact case still gives:



```text

T\_chip = 129.0 °C

Target = 85.0 °C

Margin = -44.0 °C

```



\### Compact Forced-Air Conclusion



The compact 80 × 80 × 25 mm forced-air heatsink is not sufficient for 250 W.



A copper spreader or vapor chamber cannot rescue the compact design because the dominant resistance is not spreading resistance. The dominant resistance is the air-side fin-stack resistance.



\## Architecture 3: Larger Forced-Air Heatsink



The recommended forced-air candidate was:



```text

80 × 100 × 50 mm heatsink

channel velocity = 5 m/s

fin gap = 2 mm

fin thickness = 1 mm

```



This geometry was selected from the robust forced-air sweep because it passed both analytical air-side models.



After adding TIM, base conduction, and spreading resistance, the larger forced-air candidate still passed.



| Base / spreader | T\_chip | Margin | Status |

|---|---:|---:|---|

| Aluminum 6061 | 82.4 °C | 2.6 °C | PASS |

| Aluminum high-k | 82.0 °C | 3.0 °C | PASS |

| Copper spreader | 80.9 °C | 4.1 °C | PASS |

| Vapor chamber conservative | 81.0 °C | 4.0 °C | PASS |

| Vapor chamber baseline | 80.4 °C | 4.6 °C | PASS |

| Vapor chamber optimistic | 80.2 °C | 4.8 °C | PASS |



\### Larger Forced-Air Conclusion



The 80 × 100 × 50 mm forced-air heatsink is the first architecture that meets the 85 °C chip target in the analytical screening.



It passes even with an aluminum base, although the thermal margin is small.



Copper or vapor-chamber spreading improves the margin slightly.



\## Architecture 4: Copper Spreader / Vapor-Chamber-Assisted Spreading



The vapor chamber was not modelled as a detailed two-phase device.



Instead, it was represented as an equivalent anisotropic heat spreader:



```text

kx = ky >> kz

```



This captures the main useful role of a vapor chamber: improved lateral heat spreading from the chip into the heatsink base.



The spreading-resistance model showed that for the actual project geometry, spreading resistance is small compared with air-side resistance.



For the 80 × 100 mm base:



| Material | R\_spreading | Spreading temperature penalty at 250 W |

|---|---:|---:|

| Aluminum 6061 | 0.00718 K/W | 1.80 °C |

| Copper | 0.00329 K/W | 0.82 °C |

| Vapor chamber baseline | approximately 0.0007 K/W | approximately 0.18 °C |



The improvement from aluminum to vapor chamber baseline in the recommended forced-air case was approximately:



```text

82.4 - 80.4 = 2.0 °C

```



\### Vapor Chamber Conclusion



The vapor chamber improves chip temperature and thermal margin, but the improvement is modest for this chip/base geometry.



This happens because the chip is relatively large:



```text

chip = 45 mm × 45 mm

```



and the spreading expansion is not extreme:



```text

45 × 45 mm source → 80 × 100 mm base

```



Therefore, the vapor chamber is useful mainly for:



```text

hotspot control

temperature uniformity

extra thermal margin

mechanical packaging flexibility

```



It is not a substitute for adequate airflow and fin area.



\## Dominant Thermal Bottleneck



The resistance split shows that the design is air-side dominated.



For the compact baseline:



```text

R\_air ≈ 0.3975 K/W

R\_spreading ≈ 0.0002–0.0063 K/W

```



For the recommended forced-air candidate:



```text

R\_air ≈ 0.2023 K/W

R\_spreading ≈ 0.0003–0.0072 K/W

```



In both cases:



```text

R\_air >> R\_spreading

```



Therefore, the dominant bottleneck is:



```text

air-side heat rejection through the fin stack

```



not chip-to-base spreading.



\## Verification Performed



A verification script was used to check the spreading-resistance model.



The checks were:



| Verification check | Result |

|---|---|

| Source area = base area gives R\_spreading ≈ 0 | PASS |

| R\_spreading increases as base/source area ratio increases | PASS |

| Copper gives lower R\_spreading than aluminum | PASS |



This confirms that the spreading-resistance implementation behaves physically for trend-level architecture screening.



\## Design Decision



Based on the analytical screening, the selected architecture for the next CFD stage is:



```text

80 × 100 × 50 mm forced-air aluminum heatsink

channel velocity = 5 m/s

fin gap = 2 mm

fin thickness = 1 mm

```



This case is selected because:



| Reason | Explanation |

|---|---|

| It meets the 85 °C target analytically | T\_chip ≈ 82.4 °C |

| It does not require vapor chamber to pass | simpler baseline architecture |

| It identifies the main bottleneck correctly | air-side resistance |

| It can be compared cleanly against CFD | simple geometry and physics |

| It can later be upgraded | copper or vapor chamber can be added for margin |



\## Recommended CFD Path



The next CFD work should not start with the full board immediately.



A staged CFD approach is recommended:



| CFD stage | Purpose |

|---|---|

| CFD 0: chip + TIM + heatsink + air | compare CFD against analytical model |

| CFD 1: full board with memory and VRM | include board-level thermal crosstalk |

| CFD 2: variant with copper/vapor chamber spreader | evaluate margin and hotspot improvement if needed |



The first CFD model should use the selected aluminum forced-air candidate.



\## Final Architecture-Level Conclusion



Passive/fanless cooling is not feasible for the 250 W chip.



The compact forced-air heatsink is also insufficient.



The larger 80 × 100 × 50 mm forced-air heatsink is the first architecture that meets the target analytically.



Copper and vapor chamber spreading improve thermal margin, but the design remains dominated by air-side resistance.



Therefore, the main thermal design priority is to increase effective fin area and airflow while controlling pressure drop and mechanical envelope, rather than simply replacing the base with a vapor chamber.

