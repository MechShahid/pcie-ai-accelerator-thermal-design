\# Pre-CFD Readiness Checklist



\## Purpose



This document checks whether the analytical and pre-CFD preparation work is complete before starting the first CFD model.



The goal is to avoid jumping into CFD without knowing:



\- what cooling architecture is being tested,

\- why it was selected,

\- what analytical result it should be compared against,

\- what assumptions are already known,

\- and what limitations must be clearly stated.



\## Project Target



| Item | Value |

|---|---:|

| Main chip heat load | 250 W |

| Full board heat load | 320 W |

| Inlet / ambient air temperature | 25 °C |

| Target chip temperature | 85 °C |

| Required chip-to-air resistance | 0.240 K/W |

| Chip size | 45 mm × 45 mm |

| Baseline TIM | 0.2 mm, 6 W/mK |



The required chip-to-air resistance is:



```text

R\_required = (85 - 25) / 250 = 0.240 K/W

```



\## Completed Analytical Work



| Work item | Status | Output |

|---|---:|---|

| Design specification | Done | `docs/design\_specification.md` |

| Assumptions document | Done | `docs/assumptions.md` |

| Mechanical design plan | Done | `docs/mechanical\_design\_plan.md` |

| First-order resistance model | Done | `python/thermal\_resistance\_model.py` |

| TIM sensitivity | Done | `python/tim\_sensitivity.py` |

| Airflow heat-capacity check | Done | `python/airflow\_heat\_capacity\_check.py` |

| Airflow sanity documentation | Done | `docs/airflow\_sanity\_check.md` |

| Forced-air heatsink analytical model | Done | `python/heatsink\_analytical\_model.py` |

| Forced-air design sweep | Done | `python/heatsink\_design\_sweep.py` |

| Analytical plots | Done | `python/plot\_heatsink\_results.py` |

| Passive/fanless screening | Done | `python/passive\_fanless\_heatsink\_model.py` |

| Passive/fanless documentation | Done | `docs/passive\_fanless\_screening.md` |

| Vapor-chamber spreading method | Done | `docs/vapor\_chamber\_spreading\_method.md` |

| Vapor-chamber spreading model | Done | `python/vapor\_chamber\_spreading\_model.py` |

| Spreading-model verification | Done | `python/verify\_spreading\_model.py` |

| Vapor-chamber results | Done | `docs/vapor\_chamber\_spreading\_results.md` |

| Cooling architecture tradeoff | Done | `docs/cooling\_architecture\_tradeoff.md` |

| Selected CFD case | Done | `docs/selected\_cfd\_case.md` |

| Mechanical feasibility check | Done | `docs/mechanical\_feasibility\_check.md` |



\## Cooling Architecture Decisions



| Architecture | Result | Decision |

|---|---|---|

| Passive/fanless cooling | 25–38 W at 85 °C | Rejected |

| Compact forced-air 80 × 80 × 25 mm | chip around 129–131 °C | Rejected |

| Compact + copper/vapor chamber | still fails | Rejected |

| Larger forced-air 80 × 100 × 50 mm | chip around 82.4 °C | Selected for CFD 0 |

| Larger + copper/vapor chamber | improves margin slightly | Optional later upgrade |

| Liquid cooling | not needed yet | Reserve as escalation option |



\## Selected CFD 0 Case



The selected first CFD case is:



| Parameter | Value |

|---|---:|

| Cooling method | forced-air plate-fin heatsink |

| Heatsink material | aluminum |

| Base width | 80 mm |

| Base length | 100 mm |

| Base thickness | 5 mm |

| Fin height | 50 mm |

| Fin thickness | 1 mm |

| Fin gap | 2 mm |

| Approximate number of fins | 26 |

| Chip heat load | 250 W |

| Chip size | 45 mm × 45 mm |

| TIM thickness | 0.2 mm |

| TIM conductivity | 6 W/mK |

| Inlet air temperature | 25 °C |

| Inlet/channel velocity | 5 m/s |



This is a thermal validation candidate, not a finalized PCIe product geometry.



\## Analytical Reference for CFD 0



The analytical model predicts:



| Quantity | Value |

|---|---:|

| TIM resistance | 0.0165 K/W |

| Base 1D resistance | 0.0037 K/W |

| Spreading resistance | 0.0072 K/W |

| Air-side resistance | 0.2023 K/W |

| Total resistance | 0.2297 K/W |

| Predicted chip temperature | 82.4 °C |

| Thermal margin | 2.6 °C |



The CFD result should be compared against:



```text

T\_chip,analytical ≈ 82.4 °C

```



\## Main Technical Conclusion Before CFD



The analytical work shows that the design is dominated by air-side heat rejection.



For the recommended candidate:



| Resistance term | Approximate value |

|---|---:|

| TIM | 0.0165 K/W |

| Base 1D conduction | 0.0037 K/W |

| Spreading resistance | 0.0072 K/W |

| Air-side resistance | 0.2023 K/W |



The largest resistance is:



```text

air-side fin-stack resistance

```



Therefore, the main design priority is to increase effective fin area and airflow while controlling pressure drop and mechanical envelope.



\## Mechanical Feasibility Status



The selected heatsink is mechanically aggressive.



The rough mass estimate is:



```text

approximately 0.46 kg

```



Key mechanical concerns are:



| Concern | Status |

|---|---|

| 50 mm fin height | may exceed compact PCIe envelope |

| mass | likely needs backplate/support |

| TIM pressure | must be controlled |

| mounting | four-point screw mount recommended |

| PCB bending | needs later structural check |

| airflow | requires guided/server-style ducting |



Mechanical feasibility has been documented, but detailed structural FEM is not yet done.



\## CFD 0 Scope



The first CFD model should include:



| Component | Include? |

|---|---:|

| Chip heat source | Yes |

| TIM layer | Yes |

| Aluminum heatsink base | Yes |

| Aluminum fins | Yes |

| Air domain | Yes |

| PCB | No |

| Memory chips | No |

| VRM | No |

| Full board | No |

| Vapor chamber | No |



The purpose is to validate the analytical heatsink trend before adding full-board complexity.



\## CFD 0 Boundary Conditions



| Boundary | Value |

|---|---|

| Inlet | velocity inlet |

| Inlet velocity | 5 m/s |

| Inlet temperature | 25 °C |

| Outlet | pressure outlet |

| Outlet gauge pressure | 0 Pa |

| Chip heat load | 250 W |

| Solid-fluid walls | coupled heat transfer |

| External domain walls | adiabatic or symmetry/slip depending on setup |



\## Expected CFD Outputs



The CFD result should report:



| Output | Purpose |

|---|---|

| Maximum chip temperature | compare with 85 °C target |

| Average chip temperature | compare with analytical 82.4 °C |

| Fin-base temperature | check solid conduction/spreading |

| Fin temperature distribution | check fin effectiveness |

| Outlet air temperature | compare with heat-capacity estimate |

| Pressure drop | assess airflow feasibility |

| Velocity field | check flow maldistribution |

| Temperature field | identify hotspots |

| Heat balance | confirm approximately 250 W removed by air |



\## CFD 0 Success Criteria



| Criterion | Expected |

|---|---|

| Solver convergence | stable residuals |

| Energy balance | heat removed by air ≈ 250 W |

| Chip temperature | same trend as analytical model |

| Velocity field | physical channel flow |

| Temperature field | no unrealistic hot/cold regions |

| Pressure drop | reported |



Exact agreement with the analytical model is not required. The analytical model assumes ideal guided flow, uniform effective heat-transfer coefficient, simplified fin efficiency, and equivalent circular spreading.



\## Known Limitations Before CFD



| Limitation | Meaning |

|---|---|

| Geometry is simplified | not a full PCIe board |

| Heatsink is mechanically aggressive | not final product geometry |

| Flow is guided | bypass is not yet modelled |

| Radiation excluded | acceptable for first forced-air CFD |

| TIM contact resistance ignored | bulk TIM only |

| Real chip hotspot map absent | uniform heat load assumed |

| Memory/VRM excluded | full-board crosstalk not yet included |



\## Next Action



The project is ready for CFD 0.



The next action is:



```text

Build the simplified chip + TIM + aluminum heatsink + guided-air CFD model.

```



The CFD model should use the selected thermal candidate:



```text

80 × 100 × 50 mm aluminum plate-fin heatsink

45 × 45 mm chip

0.2 mm TIM

250 W heat load

5 m/s inlet air at 25 °C

```



After CFD 0, the next stage is full-board CFD with PCB, memory, VRM, and airflow bypass/crosstalk.

