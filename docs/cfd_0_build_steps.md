\# CFD 0 Build Steps



\## Purpose



This document gives the practical build steps for the first CFD model in the PCIe AI accelerator thermal design study.



The CFD 0 model is intentionally simplified.



It includes:



```text

chip + TIM + aluminum heatsink + guided airflow

```



It does not yet include:



```text

full PCB, memory, VRM, PCIe bracket, fan model, bypass leakage, or vapor chamber

```



The goal is to compare CFD against the analytical estimate before adding full-board complexity.



\## CFD 0 Target Case



| Parameter | Value |

|---|---:|

| Chip heat load | 250 W |

| Chip size | 45 mm × 45 mm |

| Chip thickness | 2 mm |

| TIM thickness | 0.2 mm |

| TIM conductivity | 6 W/mK |

| Heatsink base | 80 mm × 100 mm × 5 mm |

| Fin height | 50 mm |

| Fin thickness | 1 mm |

| Fin gap | 2 mm |

| Approximate number of fins | 26 |

| Heatsink material | Aluminum |

| Inlet air temperature | 25 °C |

| Inlet velocity | 5 m/s |

| Outlet pressure | 0 Pa gauge |

| Target chip temperature | 85 °C |

| Analytical predicted chip temperature | about 82.4 °C |



\## Coordinate System



Use the following coordinate convention:



| Direction | Meaning |

|---|---|

| X direction | heatsink width |

| Y direction | airflow / fin length direction |

| Z direction | vertical direction / fin height direction |



So:



```text

X = 80 mm heatsink width

Y = 100 mm flow length

Z = chip/TIM/base/fin height direction

```



\## Geometry Build Order



Build the solid geometry in this order:



```text

1\. Chip

2\. TIM

3\. Heatsink base

4\. Fin array

5\. Air domain

```



This order makes it easier to check contact surfaces.



\## Step 1: Chip Geometry



Create a rectangular chip block.



| Parameter | Value |

|---|---:|

| Chip width | 45 mm |

| Chip length | 45 mm |

| Chip thickness | 2 mm |



Suggested position:



```text

Chip centered under the heatsink base.

```



For example:



| Direction | Size |

|---|---:|

| X | 45 mm |

| Y | 45 mm |

| Z | 2 mm |



The chip top face should contact the TIM bottom face.



\## Step 2: TIM Geometry



Create a thin TIM layer above the chip.



| Parameter | Value |

|---|---:|

| TIM width | 45 mm |

| TIM length | 45 mm |

| TIM thickness | 0.2 mm |



The TIM should be exactly aligned with the chip footprint.



The TIM bottom face contacts the chip.



The TIM top face contacts the heatsink base.



\## Step 3: Heatsink Base Geometry



Create the heatsink base above the TIM.



| Parameter | Value |

|---|---:|

| Base width | 80 mm |

| Base length | 100 mm |

| Base thickness | 5 mm |



The base should be centered over the chip/TIM.



The bottom face of the base contacts the top face of the TIM.



\## Step 4: Fin Array Geometry



Create straight plate fins on top of the heatsink base.



| Parameter | Value |

|---|---:|

| Fin height | 50 mm |

| Fin thickness | 1 mm |

| Fin gap | 2 mm |

| Fin length | 100 mm |

| Fin material | Aluminum |



The fins should run in the airflow direction.



Using the coordinate convention:



```text

fin length along Y

fin thickness along X

fin height along Z

```



The fin pitch is:



```text

pitch = fin thickness + fin gap

pitch = 1 mm + 2 mm

pitch = 3 mm

```



Across an 80 mm width:



```text

approximate number of fins = 26

```



A practical arrangement is:



```text

26 fins, each 1 mm thick

25 gaps between fins, each 2 mm wide

```



This uses:



```text

26 × 1 mm + 25 × 2 mm = 76 mm

```



This leaves:



```text

80 mm - 76 mm = 4 mm

```



So use approximately:



```text

2 mm side clearance on each side

```



\## Step 5: Air Domain



Create an air domain around the heatsink.



For CFD 0, use a guided/ducted air domain so that the airflow passes through the fin channels.



Suggested simple air domain:



| Direction | Suggested size |

|---|---:|

| Width X | 90 mm |

| Flow length Y | 160 mm |

| Height Z | 65 mm |



This gives:



| Region | Purpose |

|---|---|

| 30 mm inlet extension before heatsink | allow flow development |

| 100 mm heatsink length | fin region |

| 30 mm outlet extension after heatsink | allow outlet recovery |

| 50 mm fin height + 15 mm top clearance | reduce artificial blockage |

| 5 mm side clearance each side | avoid wall interference |



So the air domain can be:



```text

X = 90 mm

Y = 160 mm

Z = 65 mm

```



The heatsink should be located inside the air domain with the fin region aligned to the flow direction.



\## Step 6: Fluid-Solid Contacts



Make sure the following contacts are conformal or coupled:



| Interface | Type |

|---|---|

| Chip to TIM | solid-solid conduction |

| TIM to heatsink base | solid-solid conduction |

| Heatsink base to fins | same solid body or bonded contact |

| Heatsink surfaces to air | coupled fluid-solid wall |



For the cleanest CFD 0 setup, the heatsink base and fins can be one aluminum solid body.



\## Step 7: Materials



\### Chip



Use a simplified high-conductivity solid.



| Property | Value |

|---|---:|

| Thermal conductivity | 100–150 W/mK |



For CFD 0, exact chip material is less important than the heat load and TIM/base path.



\### TIM



| Property | Value |

|---|---:|

| Thermal conductivity | 6 W/mK |



\### Aluminum



| Property | Value |

|---|---:|

| Thermal conductivity | 167–200 W/mK |

| Density | 2700 kg/m³ |

| Specific heat | 900 J/kgK |



Use aluminum for both base and fins.



\### Air



Use air as the fluid.



For the first model, constant properties are acceptable.



Later, temperature-dependent air properties can be used.



\## Step 8: Boundary Conditions



\### Chip Heat Load



Apply:



```text

250 W

```



Options:



| Method | Recommendation |

|---|---|

| Volumetric heat generation inside chip | preferred |

| Uniform heat flux on chip/TIM interface | acceptable |



For volumetric heat generation:



Chip volume:



```text

V\_chip = 0.045 × 0.045 × 0.002

&#x20;      = 4.05e-6 m³

```



Volumetric heat generation:



```text

q''' = 250 / 4.05e-6

&#x20;    ≈ 6.17e7 W/m³

```



So use:



```text

q''' ≈ 6.17 × 10^7 W/m³

```



\### Inlet



| Parameter | Value |

|---|---:|

| Boundary type | velocity inlet |

| Velocity | 5 m/s |

| Temperature | 25 °C |



\### Outlet



| Parameter | Value |

|---|---:|

| Boundary type | pressure outlet |

| Gauge pressure | 0 Pa |



\### External Walls



For CFD 0, use a guided duct assumption.



| Wall | Suggested condition |

|---|---|

| Top air-domain wall | adiabatic wall or symmetry/slip |

| Side air-domain walls | adiabatic wall or symmetry/slip |

| Bottom outside solid region | adiabatic |



The aim is not to model a full chassis yet.



The aim is to force air through the fin channels consistently with the analytical model.



\## Step 9: Physics Models



Use steady-state conjugate heat transfer.



| Physics | Setting |

|---|---|

| Flow | steady |

| Energy equation | on |

| Solid conduction | on |

| Fluid-solid heat transfer | coupled |

| Radiation | off for CFD 0 |

| Gravity | off |

| Compressibility | incompressible / low-speed air |



Radiation is excluded in CFD 0 because this is a forced-air heatsink comparison case.



\## Step 10: Laminar or Turbulent?



The channel hydraulic diameter is approximately:



```text

Dh ≈ 3.7 mm

```



At 5 m/s, the Reynolds number is roughly:



```text

Re ≈ 1200

```



This is still not strongly turbulent.



For CFD 0, run:



```text

first run: laminar

```



Then optionally compare with:



```text

second run: low-Re turbulence model or k-omega SST

```



The first objective is not turbulence perfection. The first objective is to check whether the CFD trend matches the analytical estimate.



\## Step 11: Mesh Strategy



Use a reasonably fine mesh in:



| Region | Reason |

|---|---|

| Fin channels | velocity and thermal boundary layers |

| TIM layer | very thin conduction layer |

| Chip/TIM/base contact | high temperature gradient |

| Fin roots | conduction and convection coupling |

| Inlet/outlet extensions | stable flow field |



Important mesh guidance:



| Item | Recommendation |

|---|---|

| TIM thickness | at least 2–3 cells through thickness if meshed |

| Fin gap | several cells across 2 mm gap |

| Fin thickness | at least 2 cells across 1 mm if possible |

| Boundary layers | use inflation layers on fin surfaces |

| Mesh check | compare one coarse and one refined mesh |



If the TIM is too thin and causes meshing problems, it can later be represented as a thermal resistance boundary, but the first geometry-based model should try to include it explicitly.



\## Step 12: Solver Settings



Suggested first settings:



| Setting | Recommendation |

|---|---|

| Solver | pressure-based |

| Time | steady |

| Velocity-pressure coupling | coupled or SIMPLE |

| Energy | enabled |

| Discretization | second-order where stable |

| Initialization | hybrid/standard |

| Convergence | residuals plus heat balance |



Do not judge convergence by residuals alone.



Also monitor:



```text

maximum chip temperature

outlet air temperature

total heat removed by outlet air

pressure drop

```



\## Step 13: Results to Extract



Extract the following results:



| Result | Required? |

|---|---|

| Maximum chip temperature | Yes |

| Average chip temperature | Yes |

| Base temperature under chip | Yes |

| Maximum heatsink temperature | Yes |

| Fin temperature distribution | Yes |

| Outlet air temperature | Yes |

| Pressure drop | Yes |

| Velocity contours | Yes |

| Temperature contours | Yes |

| Heat balance | Yes |



\## Step 14: Heat Balance Check



The CFD should remove approximately:



```text

250 W

```



through the outlet air.



Use:



```text

Q\_air = m\_dot cp (T\_out - T\_in)

```



This should be close to the chip heat load.



A large mismatch means the model is not physically balanced or has incorrect boundary conditions.



\## Step 15: Compare Against Analytical Result



The analytical reference is:



```text

T\_chip ≈ 82.4 °C

```



The CFD does not need to match exactly.



Expected interpretation:



| CFD result | Meaning |

|---|---|

| near 82–90 °C | good agreement/trend |

| much higher | airflow or fin effectiveness worse than analytical assumption |

| much lower | boundary conditions may be too idealized |

| heat balance wrong | setup problem |



\## Step 16: What Not To Do in CFD 0



Do not include everything at once.



Avoid adding:



```text

full PCB

memory

VRM

fan curve

radiation

vapor chamber

complex chassis

detailed chip package

```



Those belong to later stages.



CFD 0 must stay simple so that the result can be compared to the analytical model.



\## Final CFD 0 Build Summary



Build:



```text

45 × 45 × 2 mm chip

0.2 mm TIM

80 × 100 × 5 mm aluminum base

26 aluminum fins

1 mm fin thickness

2 mm fin gap

50 mm fin height

air domain with 5 m/s inlet at 25 °C

250 W chip heat generation

pressure outlet at 0 Pa

```



Expected analytical reference:



```text

T\_chip ≈ 82.4 °C

```



Primary CFD outputs:



```text

chip temperature

outlet air temperature

pressure drop

velocity field

temperature field

heat balance

```

