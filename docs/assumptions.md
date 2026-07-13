\# Assumptions



\## Purpose of This Document



This document records the assumptions used in the simplified mechanical and thermal design workflow for the 250 W PCIe AI accelerator card.



The purpose is to clearly separate:



\- Sourced or standard-based information

\- Common engineering assumptions

\- Simplified modelling assumptions

\- Sensitivity parameters



This is important because the project is an engineering demonstrator, not a reverse-engineered commercial product.



\## Project-Level Assumptions



| Item | Assumption |

|---|---|

| Product type | Simplified PCIe AI accelerator add-in card |

| Design type | Original engineering demonstrator |

| Commercial product copying | Not used |

| Production qualification claim | Not claimed |

| Main purpose | Mechanical and thermal workflow demonstration |

| Target application | High-TDP board-level electronics cooling |



\## PCIe Form-Factor Assumptions



| Parameter | Value | Basis |

|---|---:|---|

| Card length | 167.65 mm | PCIe-style standard-height, half-length add-in-card reference |

| Card height | 111.15 mm | PCIe-style standard-height add-in-card reference |

| PCB thickness | 1.6 mm | Common engineering assumption |



The PCIe envelope is used to make the layout realistic. The project does not attempt to model every detail of the PCIe connector, bracket, chassis interface, or retention mechanism.



\## Component Geometry Assumptions



| Component | Assumed Dimension |

|---|---:|

| Main AI accelerator chip | 45 mm × 45 mm × 2 mm |

| TIM layer | 45 mm × 45 mm × 0.2 mm |

| Heatsink base | 80 mm × 80 mm × 5 mm |

| Fin height | 25 mm |

| Fin thickness | 1 mm |

| Fin spacing | 2 mm |

| Memory chip size | 14 mm × 12 mm × 1.5 mm |

| Number of memory chips | 8 |

| VRM region | 60 mm × 15 mm × 3 mm |

| Mounting holes | 4 symmetric holes around the main chip |



These dimensions are not claimed to represent a specific commercial AI accelerator. They are selected to create a realistic board-level cooling problem.



\## Heat-Load Assumptions



| Heat Source | Assumed Power |

|---|---:|

| Main AI accelerator chip | 250 W |

| Memory chips | 8 × 5 W = 40 W |

| VRM / power delivery region | 30 W |

| Total board heat load | 320 W |



The main thermal design challenge is the 250 W accelerator chip. Memory and VRM heat loads are included to avoid an unrealistically isolated chip-only model.



\## Thermal Target Assumptions



| Quantity | Value |

|---|---:|

| Inlet air temperature | 25°C |

| Target maximum chip case temperature | 85°C |

| Allowed chip temperature rise | 60°C |

| Required chip-to-air thermal resistance | 0.24 K/W |



The required chip-to-air thermal resistance is calculated as:



```text

R\_required = (T\_chip,max - T\_air,inlet) / Q\_chip

