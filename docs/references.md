\# References



\## Purpose of This Document



This document records the sources and reference categories used for the simplified mechanical and thermal design workflow of a 250 W PCIe AI accelerator card.



The goal is to clearly separate sourced information from engineering assumptions.



This project is an original engineering demonstrator. It is not copied from a commercial accelerator card.



\## Reference Categories



The project uses four types of references:



| Category | Meaning |

|---|---|

| Standard / form-factor reference | Used for PCIe-style card envelope dimensions |

| Engineering handbook / material reference | Used for typical material properties |

| Vendor datasheet / product reference | Used only when a specific value is taken from a public datasheet |

| Engineering assumption | Used when no product-specific source is available |



\## PCIe Form-Factor References



The baseline model uses a PCIe-style standard-height, half-length add-in card envelope.



| Parameter | Value | Reference Type |

|---|---:|---|

| Card length | 167.65 mm | PCIe add-in-card form-factor reference |

| Card height | 111.15 mm | PCIe add-in-card form-factor reference |

| PCB thickness | 1.6 mm | Common PCB engineering assumption |



These values define the simplified mechanical envelope only. The project does not model the complete PCIe connector, bracket retention feature, chassis interface, or compliance details.



\## M.2 Context References



M.2 is included only as context for compact accelerator modules.



| M.2 Type | Width | Length |

|---|---:|---:|

| M.2 2280 | 22 mm | 80 mm |



M.2 is not the main focus of the first project version. It may be considered later as an optional compact-module extension.



\## Material Property References



The following material values are used as first-version assumptions and should be replaced by specific datasheet values if a later detailed model requires it.



| Material | Typical Thermal Conductivity Range |

|---|---:|

| FR4 through-plane equivalent | approximately 0.3 W/mK |

| Silicon | approximately 100 to 150 W/mK |

| Aluminum 6061 / 6063 | approximately 167 to 200 W/mK |

| Copper | approximately 385 to 400 W/mK |

| TIM | 3, 6, 8 W/mK sensitivity values |



\## Thermal Design Reference Equations



\### Required Chip-to-Air Thermal Resistance



```text

R\_required = (T\_chip,max - T\_air,inlet) / Q\_chip

