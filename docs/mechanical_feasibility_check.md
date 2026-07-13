\# Mechanical Feasibility Check



\## Purpose



This document records the first mechanical feasibility check for the selected thermal candidate in the PCIe AI accelerator cooling study.



The analytical thermal work identified the following forced-air heatsink as the first passing thermal candidate:



```text

80 mm × 100 mm × 50 mm aluminum plate-fin heatsink

5 mm base thickness

50 mm fin height

2 mm fin gap

1 mm fin thickness

5 m/s guided airflow

250 W chip heat load

```



This geometry is thermally promising, but it is not yet a mechanically finalized PCIe product design.



The purpose of this note is to identify the main mechanical risks before moving to CFD.



\## Selected Thermal Candidate



| Parameter | Value |

|---|---:|

| Heatsink base width | 80 mm |

| Heatsink base length | 100 mm |

| Base thickness | 5 mm |

| Fin height | 50 mm |

| Fin thickness | 1 mm |

| Fin gap | 2 mm |

| Approximate number of fins | 26 |

| Material | Aluminum |

| Chip size | 45 mm × 45 mm |

| Chip heat load | 250 W |

| TIM thickness target | 0.2 mm |

| Nominal channel velocity | 5 m/s |



\## Mechanical Status of This Geometry



The selected heatsink should be treated as:



```text

a thermal performance candidate

```



not as:



```text

a finalized PCIe mechanical product design

```



This distinction is important because the 50 mm fin height may be too large for some PCIe card envelopes depending on the system chassis, adjacent slot spacing, airflow ducting, and mechanical support strategy.



\## Key Mechanical Risks



| Risk | Why it matters |

|---|---|

| Heatsink height | 50 mm fins may exceed compact PCIe slot constraints |

| Heatsink mass | Large aluminum heatsink may load the PCB mechanically |

| PCB bending | Heavy heatsink and screw preload can bend the board |

| TIM bond-line control | TIM resistance depends on compression, flatness, and preload |

| Mounting method | Poor mounting can cause high contact resistance or board damage |

| Keepout area | Memory, VRM, capacitors, connectors, and inductors may limit heatsink footprint |

| Airflow ducting | 5 m/s channel velocity requires a guided/server-style airflow path |

| Vibration/shock | Large heatsink may require additional mechanical support |

| Manufacturing tolerance | Flatness and surface finish affect TIM/contact performance |



\## Rough Heatsink Mass Estimate



A first mass estimate can be made from:



```text

mass = density × solid volume

```



For aluminum:



```text

density ≈ 2700 kg/m³

```



The solid volume is approximated as:



```text

V\_total = V\_base + V\_fins

```



\### Base Volume



```text

V\_base = width × length × base thickness

```



Using:



```text

width = 80 mm = 0.080 m

length = 100 mm = 0.100 m

base thickness = 5 mm = 0.005 m

```



gives:



```text

V\_base = 0.080 × 0.100 × 0.005

&#x20;      = 0.000040 m³

```



The base mass is:



```text

m\_base = 2700 × 0.000040

&#x20;      ≈ 0.108 kg

&#x20;      ≈ 108 g

```



\### Fin Volume



Approximate fin volume:



```text

V\_fins = number of fins × fin thickness × fin height × fin length

```



Using:



```text

number of fins ≈ 26

fin thickness = 1 mm = 0.001 m

fin height = 50 mm = 0.050 m

fin length = 100 mm = 0.100 m

```



gives:



```text

V\_fins = 26 × 0.001 × 0.050 × 0.100

&#x20;      = 0.000130 m³

```



The fin mass is:



```text

m\_fins = 2700 × 0.000130

&#x20;      ≈ 0.351 kg

&#x20;      ≈ 351 g

```



\### Approximate Total Mass



```text

m\_total = m\_base + m\_fins

&#x20;       ≈ 108 g + 351 g

&#x20;       ≈ 459 g

```



So the selected heatsink has an approximate aluminum mass of:



```text

about 0.46 kg

```



This is significant for a PCB-mounted component and likely requires a robust mounting strategy.



\## Mechanical Interpretation of Mass



A heatsink mass of roughly 0.46 kg is not impossible, but it is high enough that the design should not rely only on the chip package or PCB solder joints for support.



The design should include:



| Feature | Purpose |

|---|---|

| Backplate | reduce PCB bending under heatsink load and screw preload |

| Four-point mounting | distribute load around the chip |

| Spring screws | control TIM pressure and avoid overloading the package |

| Compression stops | prevent excessive TIM squeeze-out or chip damage |

| Optional chassis support | reduce vibration and bending loads |



\## Mounting Concept



The baseline mechanical concept is:



```text

heatsink

↓

TIM

↓

chip/package

↓

PCB

↓

backplate

```



Recommended attachment method:



| Item | Recommendation |

|---|---|

| Mounting points | four screws around the chip |

| Preload control | spring-loaded screws |

| Backside support | metal backplate |

| TIM bond line | controlled around 0.2 mm |

| Contact pressure | sufficient for TIM wetting but limited to avoid package damage |

| Electrical isolation | use insulating washers or coating if required |



\## TIM Mechanical Control



The TIM thermal resistance used in the analytical model assumes:



```text

TIM thickness = 0.2 mm

TIM conductivity = 6 W/mK

```



However, actual TIM performance depends on:



| Factor | Effect |

|---|---|

| Bond-line thickness | thicker TIM increases resistance |

| Contact pressure | improves wetting and reduces voids |

| Surface flatness | affects local contact quality |

| Surface roughness | affects interface resistance |

| Pump-out / ageing | can degrade long-term performance |

| Mounting preload | controls compression and repeatability |



Therefore, the mechanical design must control TIM thickness and pressure.



The TIM resistance in the analytical model should be interpreted as a controlled bulk TIM resistance, not a complete contact-resistance model.



\## PCIe Envelope Concern



The selected heatsink is thermally useful but mechanically aggressive.



The 50 mm fin height may conflict with:



| Constraint | Possible issue |

|---|---|

| Adjacent PCIe slots | may block nearby slots |

| Server chassis height | may exceed available clearance |

| Add-in-card mechanical limits | may require bracket or chassis support |

| Airflow duct | may need custom shroud |

| Connector/edge clearance | must preserve PCIe connector region |



Therefore, this geometry should be labelled as a:



```text

performance-envelope CFD candidate

```



not a final compact PCIe product.



\## Airflow Mechanical Requirement



The analytical model assumes approximately:



```text

5 m/s guided channel velocity

```



This requires a realistic mechanical airflow path.



Possible implementation options:



| Option | Description |

|---|---|

| Server-style duct | air is forced directly through fin channels |

| Shroud | reduces bypass around the heatsink |

| Fan wall / chassis fan | provides system-level airflow |

| Local blower | possible but adds noise, power, and reliability concerns |



The CFD model should therefore start with a guided-flow assumption and later test bypass or duct leakage.



\## Keepout and Board Integration



The current thermal candidate uses an 80 mm × 100 mm heatsink footprint.



Before full-board CFD or CAD finalization, the following must be checked:



| Item | Check |

|---|---|

| Memory placement | does heatsink overlap memory packages? |

| VRM region | does heatsink block inductors or MOSFETs? |

| Capacitors | are tall components inside the footprint? |

| PCIe bracket | does the heatsink interfere with bracket geometry? |

| Power connector | is clearance available? |

| Board edge | does the heatsink exceed card outline? |

| Screw holes | can four mounting points fit around chip? |



\## Structural FEM Plan



Detailed structural FEM is not required before the first CFD model.



It should be done after the thermal candidate is stable.



Recommended FEM checks:



| FEM check | Purpose |

|---|---|

| Static PCB bending | check deflection due to heatsink mass and mounting preload |

| Backplate effectiveness | compare PCB bending with and without backplate |

| Screw preload sensitivity | check chip/TIM compression and board stress |

| Heatsink gravity loading | estimate stress under vertical/horizontal orientation |

| Simple modal check | identify low-frequency vibration risk |

| Shock/vibration concept check | optional portfolio extension |



\## CFD Implication



The first CFD model can use the selected 80 × 100 × 50 mm geometry because it is a useful thermal validation case.



However, the CFD result should be reported with the following caution:



```text

This CFD geometry is a thermal performance candidate. Mechanical envelope, mounting, mass, and board-integration constraints require further design refinement before it can be treated as a finalized PCIe product geometry.

```



\## Mechanical Design Conclusion



The selected 80 × 100 × 50 mm aluminum heatsink is thermally promising but mechanically aggressive.



The rough mass estimate is approximately:



```text

0.46 kg

```



This mass and the 50 mm fin height mean that the design likely requires:



```text

backplate support

four-point screw mounting

spring preload control

TIM bond-line control

guided airflow ducting

possible chassis support

```



The next CFD model can proceed using this geometry, but the project should clearly distinguish between:



```text

thermal validation candidate

```



and:



```text

mechanically finalized product design

```

