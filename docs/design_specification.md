\# Design Specification



\## Project Title



Mechanical and Thermal Design Workflow for a 250 W PCIe AI Accelerator Card



\## Purpose



This document defines the baseline design specification for a simplified PCIe-style AI accelerator card.



The project is intended to demonstrate an engineering workflow for board-level electronics cooling, mechanical layout assessment, thermal resistance estimation, CFD planning, and validation thinking.



This is an original engineering demonstrator. It is not copied from any commercial accelerator card and does not claim production qualification.



\## Design Objective



The objective is to design and assess a simplified forced-air cooled PCIe AI accelerator card with:



\- A high-power AI accelerator chip

\- Board-level memory components

\- VRM / power delivery region

\- Aluminum heatsink

\- TIM layer

\- PCIe-style mechanical envelope

\- Forced-air cooling path

\- Mounting-hole and PCB-deflection considerations

\- CFD-ready geometry and boundary conditions



The project should show practical electronics cooling judgement, not only simulation execution.



\## Baseline Card Form Factor



The baseline model represents a standard-height, half-length PCIe add-in card.



| Parameter | Value |

|---|---:|

| Card length | 167.65 mm |

| Card height | 111.15 mm |

| PCB thickness | 1.6 mm |



The PCIe card dimensions are treated as sourced form-factor dimensions. The PCB thickness is treated as a common engineering assumption for this simplified model.



\## Baseline Component Geometry



| Component | Baseline Dimension |

|---|---:|

| Main AI accelerator chip | 45 mm × 45 mm × 2 mm |

| TIM layer | 45 mm × 45 mm × 0.2 mm |

| Heatsink base | 80 mm × 80 mm × 5 mm |

| Fin height | 25 mm |

| Fin thickness | 1 mm |

| Fin spacing | 2 mm |

| Memory chips | 8 blocks around main chip |

| Memory chip size | 14 mm × 12 mm × 1.5 mm each |

| VRM region | 60 mm × 15 mm × 3 mm |

| Mounting holes | 4 symmetric holes around main chip |

| Airflow direction | Along heatsink fins |



These component dimensions are engineering assumptions selected to create a realistic board-level cooling demonstrator.



\## Baseline Heat Loads



| Heat Source | Power |

|---|---:|

| Main AI accelerator chip | 250 W |

| Memory chips | 8 × 5 W = 40 W |

| VRM / power delivery region | 30 W |

| Total board heat load | 320 W |



The main design focus is the 250 W accelerator chip. Memory and VRM heat loads are included to make the model more representative of a real board-level electronics cooling problem.



\## Thermal Design Targets



| Quantity | Value |

|---|---:|

| Ambient inlet air temperature | 25°C |

| Target maximum chip case temperature | 85°C |

| Allowed chip temperature rise | 60°C |

| Required chip-to-air thermal resistance | 0.24 K/W |



The required chip-to-air thermal resistance is calculated as:



```text

R\_required = (T\_chip,max - T\_air,inlet) / Q\_chip

