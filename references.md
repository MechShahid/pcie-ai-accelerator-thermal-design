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

## Liquid and Immersion Cooling Screening References

A liquid and immersion cooling extension was added as a screening-level comparison to the forced-air PCIe accelerator workflow.

This extension uses first-principles heat-balance equations, representative fluid properties, and simplified empirical heat-transfer correlations. It is not based on a specific commercial immersion system, pump, dielectric coolant product, or cold-plate datasheet.

### Reference status

| Item | Reference status |
|---|---|
| Heat balance equation | Standard first-law steady-flow heat balance |
| Reynolds number | Standard fluid mechanics definition |
| Prandtl number | Standard heat-transfer definition |
| Nusselt-number use | Standard convective heat-transfer formulation |
| Flat-plate forced-convection correlation | Standard empirical heat-transfer correlation |
| Laminar thermal entrance length | Standard internal-flow heat-transfer estimate |
| Fin efficiency equation | Standard extended-surface heat-transfer model |
| Air properties | Representative values near room temperature from standard property tables |
| Water-like coolant properties | Representative water properties near room temperature from standard property tables |
| Dielectric-liquid properties | Representative engineering assumptions based on typical single-phase immersion-coolant ranges |
| Cold-plate geometry | Engineering assumption |
| Immersion flow gap | Engineering assumption |
| Finned spreader geometry | Engineering assumption |
| CFD-3 reference | Internal project CFD result |

---

### Coolant heat-carrying capacity

The required coolant flow rate is estimated from the steady heat balance:

```text
Q = m_dot cp ΔT
```

where:

| Symbol | Meaning |
|---|---|
| Q | heat load |
| m_dot | coolant mass flow rate |
| cp | coolant specific heat capacity |
| ΔT | bulk coolant temperature rise |

This is a standard first-law energy-balance relation for estimating the flow required to carry a specified heat load with a specified bulk coolant temperature rise.

Reference category: standard heat-transfer textbook / first-principles thermodynamics.

---

### Dimensionless groups

The Reynolds number is calculated as:

```text
Re = rho V L / mu
```

For internal channel flow, the characteristic length is the hydraulic diameter:

```text
Re = rho V Dh / mu
```

The Prandtl number is calculated as:

```text
Pr = cp mu / k
```

The convective heat-transfer coefficient is estimated from:

```text
h = Nu k / L
```

or, for internal flow:

```text
h = Nu k / Dh
```

Reference category: standard fluid mechanics and convective heat-transfer definitions.

---

### Direct-to-chip cold-plate screening

The cold-plate estimate uses a simplified internal-flow minichannel model.

Baseline cold-plate geometry:

| Parameter | Value | Reference status |
|---|---:|---|
| Active region | approximately 50 mm × 50 mm | Engineering assumption |
| Number of channels | 10 | Engineering assumption |
| Channel width | 2 mm | Engineering assumption |
| Channel height | 1 mm | Engineering assumption |
| Channel length | 50 mm | Engineering assumption |
| Hydraulic diameter | 1.333 mm | Calculated from assumed geometry |

For the baseline laminar rectangular minichannel case, a constant screening value of:

```text
Nu = 4.12
```

is used.

This represents a simplified fully developed laminar rectangular-duct assumption for the selected aspect ratio. It is used only as a screening value and should not be interpreted as an optimized cold-plate design correlation.

The approximate laminar thermal entrance length is estimated as:

```text
L_th ≈ 0.05 Re Pr Dh
```

This is used only as a warning check. In the baseline cold-plate case, the estimated thermal entrance length is larger than the channel length, so developing-flow effects may be important.

Reference category: standard internal-flow heat-transfer textbook correlation.

---

### Single-phase immersion cooling screening

The single-phase dielectric immersion cases use a simplified laminar external forced-convection flat-plate correlation:

```text
Nu_L = 0.664 Re_L^0.5 Pr^(1/3)
```

The heat-transfer coefficient is then estimated using:

```text
h = Nu_L k / L
```

This correlation is used only for first-pass comparison between:

- bare chip-area immersion,
- idealized spreader-only immersion,
- idealized finned immersed heat-spreader screening.

The model does not represent:

- full immersion-tank CFD,
- natural convection,
- boiling,
- pump selection,
- inter-fin channel flow,
- pressure drop,
- experimental validation.

Reference category: standard external forced-convection heat-transfer textbook correlation.

---

### Fin efficiency equation

The finned immersion heat-spreader case uses a straight rectangular fin efficiency approximation:

```text
eta = tanh(mL) / (mL)
```

with:

```text
m = sqrt(2h / (k_fin t))
```

where:

| Symbol | Meaning |
|---|---|
| eta | fin efficiency |
| h | convective heat-transfer coefficient |
| k_fin | fin thermal conductivity |
| t | fin thickness |
| L | fin height |

This is used to avoid treating all fin area as perfectly effective. The model still does not resolve detailed inter-fin flow or pressure drop.

Reference category: standard extended-surface heat-transfer textbook model.

---

### Representative fluid properties used

The fluid properties are representative screening values and are not tied to one exact commercial product.

| Fluid | Density [kg/m³] | cp [J/kgK] | Dynamic viscosity [Pa·s] | Thermal conductivity [W/mK] | Reference status |
|---|---:|---:|---:|---:|---|
| Air | 1.20 | 1006 | 1.85e-5 | 0.026 | Representative near-room-temperature air properties |
| Water-like coolant | 997 | 4180 | 8.90e-4 | 0.60 | Representative near-room-temperature water properties |
| Representative dielectric liquid | 1400 | 1500 | 4.00e-3 | 0.12 | Representative dielectric-fluid screening assumption |

The air and water-like coolant values are standard near-room-temperature engineering-property values. For a more formal version, these should be checked against NIST or another standard thermophysical-property database at the selected reference temperature.

The dielectric-liquid values are intentionally labelled as representative assumptions. Real immersion fluids vary by product family and temperature. Vendor data for single-phase immersion fluids show that density, viscosity, heat capacity, and thermal conductivity are product-dependent, so a later detailed model should replace the representative values with a specific coolant datasheet.

---

### Internal project reference

The air-cooled CFD-3 result is used as an internal project reference only.

| Quantity | Value |
|---|---:|
| CFD-3 maximum chip temperature | 83.52 °C |
| CFD-3 chip rise above 25 °C inlet | 58.52 K |
| CFD-3 pressure drop | 49.02 Pa |

The CFD-3 result is a system-level ANSYS Fluent conjugate heat-transfer result. It includes the chip, TIM, heatsink, and air flow. The liquid and immersion cases are component-level convective screening estimates. Therefore, CFD-3 should not be treated as a directly equivalent bar in the liquid/immersion component-level comparison.

---

### Bibliography / sources to cite

The following sources support the equations, correlations, and property assumptions used in the liquid and immersion screening extension.

1. Incropera, F. P., DeWitt, D. P., Bergman, T. L., and Lavine, A. S.  
   *Fundamentals of Heat and Mass Transfer*.  
   Used for standard heat-transfer definitions, forced-convection correlations, internal-flow concepts, and fin-efficiency relations.

2. Çengel, Y. A., and Ghajar, A. J.  
   *Heat and Mass Transfer: Fundamentals and Applications*.  
   Used as a general reference for convection, heat balance, dimensionless numbers, internal flow, external flow, and extended surfaces.

3. White, F. M.  
   *Fluid Mechanics*.  
   Used as a general reference for Reynolds number, hydraulic diameter, and internal-flow regime interpretation.

4. NIST thermophysical-property resources.  
   Used as a preferred source category for air and water thermophysical properties when formal property values are required.

5. Engineering Toolbox air and water property tables.  
   Used as practical engineering-property tables for approximate near-room-temperature air and water values.

6. Vendor technical data sheets for single-phase immersion fluids, such as FUCHS and Shell immersion-cooling fluids.  
   Used only to justify the statement that dielectric-fluid properties are product-dependent. The current model does not use one exact commercial coolant product.
