\# Selected CFD Case



\## Purpose



This document defines the first CFD case for the PCIe AI accelerator thermal design study.



The CFD model should not start with the full board immediately. The first CFD case should validate the analytical heatsink model using a simplified chip + TIM + heatsink + forced-air domain.



The goal is to check whether the analytical trend is reasonable before adding full board details such as memory, VRM, PCB conduction, bypass flow, and board-level thermal crosstalk.



\## Selected Cooling Architecture



The selected architecture for the first CFD case is:



| Item | Selected value |

|---|---:|

| Cooling method | Forced-air heatsink |

| Base/spreader material | Aluminum |

| Heatsink base size | 80 mm × 100 mm |

| Base thickness | 5 mm |

| Fin height | 50 mm |

| Fin thickness | 1 mm |

| Fin gap | 2 mm |

| Nominal channel velocity | 5 m/s |

| Chip heat load | 250 W |

| Chip size | 45 mm × 45 mm |

| Inlet air temperature | 25 °C |

| Target chip temperature | 85 °C |



This case was selected because it was the first practical forced-air architecture that passed the analytical screening without requiring a vapor chamber.



\## Analytical Reference Result



The analytical chip-to-air resistance model predicted:



| Quantity | Value |

|---|---:|

| TIM resistance | 0.0165 K/W |

| Base 1D conduction resistance | 0.0037 K/W |

| Spreading resistance | 0.0072 K/W |

| Air-side resistance | 0.2023 K/W |

| Total resistance | 0.2297 K/W |

| Predicted chip temperature | 82.4 °C |

| Thermal margin to 85 °C | 2.6 °C |



The analytical model indicates that the design is mainly air-side dominated.



Therefore, the CFD model should focus on:



\- actual airflow distribution through the fin channels,

\- pressure drop,

\- fin temperature distribution,

\- local chip/base temperature,

\- bypass or recirculation if present,

\- difference between ideal guided flow and real 3D flow.



\## CFD Stage 0 Scope



The first CFD model should include only:



| Component | Include? |

|---|---:|

| Chip heat source | Yes |

| TIM layer | Yes |

| Aluminum heatsink base | Yes |

| Aluminum fins | Yes |

| Surrounding air domain | Yes |

| PCB | No |

| Memory chips | No |

| VRM components | No |

| Full PCIe card | No |

| Vapor chamber | No |



The purpose is to compare a simple CFD result against the analytical model.



\## Geometry Definition



\### Chip



| Parameter | Value |

|---|---:|

| Width | 45 mm |

| Length | 45 mm |

| Thickness | 2 mm, simplified |

| Heat load | 250 W |



The chip can be modelled as a solid block with volumetric heat generation, or as a heat-flux patch at the chip/TIM interface.



For the first CFD model, a uniform heat load is acceptable.



\### TIM



| Parameter | Value |

|---|---:|

| Width | 45 mm |

| Length | 45 mm |

| Thickness | 0.2 mm |

| Thermal conductivity | 6 W/mK |



The TIM should be placed between the chip and the heatsink base.



\### Heatsink Base



| Parameter | Value |

|---|---:|

| Width | 80 mm |

| Length | 100 mm |

| Thickness | 5 mm |

| Material | Aluminum |

| Thermal conductivity | 167–200 W/mK |



Use aluminum as the baseline material.



\### Fins



| Parameter | Value |

|---|---:|

| Fin height | 50 mm |

| Fin thickness | 1 mm |

| Fin gap | 2 mm |

| Fin length | 100 mm |

| Fin material | Aluminum |



The fins should be straight plate fins aligned with the forced airflow direction.



The nominal fin pitch is:



```text

pitch = fin thickness + fin gap = 1 mm + 2 mm = 3 mm

```



Across an 80 mm width, this gives approximately:



```text

number of fins ≈ 26

```



This is consistent with the analytical sweep.



\## Air Domain



The air domain should be large enough to avoid artificial blockage.



A first simple domain can be:



| Direction | Suggested domain size |

|---|---:|

| Width direction | heatsink width + side clearance |

| Flow direction | inlet extension + heatsink length + outlet extension |

| Height direction | fin height + top clearance |



For the first CFD case, use a guided/ducted-flow assumption so that air is forced through the fin channels.



This keeps the CFD boundary condition consistent with the analytical model.



\## Boundary Conditions



\### Inlet



| Parameter | Value |

|---|---:|

| Type | velocity inlet |

| Velocity | 5 m/s |

| Temperature | 25 °C |



The inlet velocity should be aligned with the fin-channel direction.



\### Outlet



| Parameter | Value |

|---|---:|

| Type | pressure outlet |

| Gauge pressure | 0 Pa |



\### Walls



| Surface | Boundary condition |

|---|---|

| Chip/TIM/base interfaces | coupled solid-solid conduction |

| Base/fin to air | coupled solid-fluid heat transfer |

| External air-domain walls | adiabatic or symmetry/slip, depending on domain setup |

| Inlet and outlet | flow boundaries |



\## Material Properties



\### Aluminum



Use:



| Property | Value |

|---|---:|

| Thermal conductivity | 167–200 W/mK |

| Density | approximately 2700 kg/m³ |

| Specific heat | approximately 900 J/kgK |



\### TIM



Use:



| Property | Value |

|---|---:|

| Thermal conductivity | 6 W/mK |

| Density | simplified/default acceptable |

| Specific heat | simplified/default acceptable |



For steady-state CFD, TIM density and specific heat are not important unless transient simulation is performed.



\### Air



Use temperature-dependent air properties if available.



For first-order steady CFD, constant air properties near 25–60 °C are acceptable.



\## Solver Type



Use a steady-state conjugate heat transfer model.



The simulation should solve:



| Physics | Include? |

|---|---:|

| Fluid flow | Yes |

| Energy equation | Yes |

| Solid conduction | Yes |

| Conjugate heat transfer | Yes |

| Radiation | No for first forced-air CFD |

| Turbulence | depends on Reynolds number and solver setup |



The analytical Reynolds number in the fin channels was in the transitional/low range for the selected geometry. For the first CFD, laminar or low-Re turbulence treatment can be tested.



A simple first run can use laminar flow if the channel Reynolds number remains low. A later sensitivity can compare laminar and turbulence models.



\## Expected CFD Outputs



The CFD result should report:



| Output | Why needed |

|---|---|

| Maximum chip temperature | compare to 85 °C target |

| Average chip temperature | compare to analytical estimate |

| Base temperature under chip | check spreading behavior |

| Fin-root temperature | compare with air-side model |

| Outlet air temperature | compare with heat-capacity check |

| Pressure drop | assess airflow feasibility |

| Velocity contours | identify maldistribution or bypass |

| Temperature contours | identify hotspots |



\## Comparison with Analytical Model



The CFD result should be compared against:



```text

Analytical predicted chip temperature ≈ 82.4 °C

```



A reasonable first CFD result may not match exactly because the analytical model assumes:



\- uniform channel velocity,

\- uniform effective heat-transfer coefficient,

\- simplified fin efficiency,

\- equivalent circular spreading approximation,

\- ideal guided flow through channels,

\- no bypass or recirculation.



If CFD gives a higher chip temperature, possible reasons include:



\- non-uniform airflow,

\- entrance effects,

\- lower effective fin area,

\- bypass around fin channels,

\- local spreading limitations,

\- higher pressure drop reducing actual flow rate.



If CFD gives a lower chip temperature, possible reasons include:



\- more effective 3D heat spreading,

\- stronger local convection,

\- optimistic boundary setup,

\- excessive domain constraint forcing ideal channel flow.



\## CFD Success Criteria



The CFD case is considered successful if it provides:



| Criterion | Target |

|---|---|

| Solver convergence | stable residuals and heat balance |

| Energy balance | heat removed by air approximately equals 250 W |

| Chip temperature | near analytical trend |

| Pressure drop | reported |

| Temperature field | physically reasonable |

| Velocity field | physically reasonable |



The CFD does not need to be production-perfect. It is used to validate the analytical trend and prepare for a more complete full-board simulation.



\## Next Stage After CFD 0



After the simplified CFD model is working, the next stage is:



```text

CFD 1: full board model with PCB, memory chips, VRM heat load, and board-level airflow.

```



The full-board model should include:



| Component | Heat load |

|---|---:|

| Main AI chip | 250 W |

| Memory chips | 40 W total |

| VRM region | 30 W |

| Total board heat load | 320 W |



This second stage will check whether nearby components and board-level airflow constraints reduce the thermal margin.

