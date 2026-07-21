# References

## Purpose of This Document

This document records the sources and reference categories used for the simplified mechanical and thermal design workflow of a 250 W PCIe AI accelerator card.

The goal is to clearly separate sourced information from engineering assumptions.

This project is an original engineering demonstrator. It is not copied from a commercial accelerator card.

---

## Reference Categories

The project uses the following reference categories:

| Category | Meaning |
|---|---|
| Standard / form-factor reference | Used for PCIe-style card envelope dimensions |
| Standard equation / correlation | Used for heat-transfer and fluid-mechanics relations such as Reynolds number, Nusselt number, flat-plate convection, and fin efficiency |
| Engineering handbook / material reference | Used for typical material and fluid properties |
| Vendor datasheet / product reference | Used only when a specific value is taken from a public datasheet |
| Internal project result | Used for results produced within this repository, such as CFD-3 chip temperature, pressure drop, and heat-balance outputs |
| Engineering assumption | Used when no product-specific source is available |

---

## PCIe Form-Factor References

The baseline model uses a PCIe-style standard-height, half-length add-in card envelope.

| Parameter | Value | Reference type |
|---|---:|---|
| Card length | 167.65 mm | PCIe add-in-card form-factor reference |
| Card height | 111.15 mm | PCIe add-in-card form-factor reference |
| PCB thickness | 1.6 mm | Common PCB engineering assumption |

These values define the simplified mechanical envelope only. The project does not model the complete PCIe connector, bracket retention feature, chassis interface, or compliance details.

---

## M.2 Context References

M.2 is included only as context for compact accelerator modules.

| M.2 type | Width | Length |
|---|---:|---:|
| M.2 2280 | 22 mm | 80 mm |

M.2 is not the main focus of the first project version. It may be considered later as an optional compact-module extension.

---

## Material Property References

The following material values are used as first-version assumptions and should be replaced by specific datasheet values if a later detailed model requires it.

| Material | Typical thermal conductivity range | Reference status |
|---|---:|---|
| FR4 through-plane equivalent | approximately 0.3 W/mK | Engineering handbook / typical PCB assumption |
| Silicon | approximately 100 to 150 W/mK | Engineering handbook / semiconductor material reference |
| Aluminium 6061 / 6063 | approximately 167 to 200 W/mK | Engineering handbook / material reference |
| Copper | approximately 385 to 400 W/mK | Engineering handbook / material reference |
| TIM | 3, 6, 8 W/mK sensitivity values | Engineering assumption / sensitivity range |

---

## Thermal Design Reference Equations

### Required chip-to-air thermal resistance

The required chip-to-air thermal resistance is calculated as:

```text
R_required = (T_chip,max - T_air,inlet) / Q_chip
```

For this project:

```text
R_required = (85 - 25) / 250
R_required = 0.24 K/W
```

This is a standard thermal-resistance sizing relation used for first-order electronics cooling estimates.

Reference category: standard heat-transfer equation.

---

## Airflow Heat-Carrying Capacity

The airflow heat-carrying capacity is estimated from:

```text
Q = m_dot cp ΔT
```

where:

| Symbol | Meaning |
|---|---|
| Q | heat load |
| m_dot | air mass flow rate |
| cp | specific heat capacity |
| ΔT | bulk air temperature rise |

This relation is used for first-pass airflow sanity checks.

Reference category: standard first-law steady-flow heat balance.

---

## Forced-Air Heatsink Screening References

The analytical forced-air heatsink screening uses simplified heat-transfer and airflow calculations to estimate whether a candidate aluminium finned heatsink can meet the 250 W chip-level cooling target.

The simplified heatsink screening includes:

- thermal-resistance estimation,
- airflow heat-capacity checks,
- fin-channel heat-transfer estimates,
- pressure-drop sanity checks,
- sensitivity to TIM conductivity and thickness,
- sensitivity to airflow velocity.

These calculations are used only for first-pass candidate selection before CFD. They are not treated as final product validation.

Reference category: standard electronics-cooling and heat-transfer textbook methods.

---

## CFD Reference Status

The CFD cases in this repository are internal project results.

| Case | Status | Reference type |
|---|---|---|
| CFD-0 | First-pass forced-air reference case | Internal project result |
| CFD-1 | Reduced-height open/bypass case | Internal project result |
| CFD-2 | Reduced-height ducted 100 mm case | Internal project result |
| CFD-3 | Reduced-height ducted 120 mm final thermal candidate | Internal project result |

The CFD-3 result is used later as a system-level reference for comparison with the liquid and immersion screening extension.

| Quantity | CFD-3 value |
|---|---:|
| Maximum chip temperature | 83.52 °C |
| Chip rise above 25 °C inlet | 58.52 K |
| Pressure drop | 49.02 Pa |

The CFD-3 result is a system-level ANSYS Fluent conjugate heat-transfer result. It includes chip, TIM, heatsink, and airflow effects.

---

## Mechanical Support Screening References

The concept-level mechanical support screening estimates heatsink volume, mass, weight force, and approximate bending moment.

The simplified bending moment is estimated as:

```text
M = W L
```

where:

| Symbol | Meaning |
|---|---|
| M | approximate bending moment |
| W | heatsink weight force |
| L | assumed lever arm |

This is only a first-pass mechanical support check. It is not a detailed PCB structural FEA, PCIe compliance check, shock/vibration assessment, or bracket design.

Reference category: first-order mechanics / engineering assumption.

---

# Liquid and Immersion Cooling Screening References

A liquid and immersion cooling extension was added as a screening-level comparison to the forced-air PCIe accelerator workflow.

This extension uses first-principles heat-balance equations, representative fluid properties, and simplified empirical heat-transfer correlations. It is not based on a specific commercial immersion system, pump, dielectric coolant product, or cold-plate datasheet.

---

## Liquid Cooling Reference Status

| Item | Reference status |
|---|---|
| Heat balance equation | Standard first-law steady-flow heat balance |
| Reynolds number | Standard fluid-mechanics definition |
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

## Coolant Heat-Carrying Capacity

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

## Dimensionless Groups

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

## Direct-to-Chip Cold-Plate Screening

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

## Single-Phase Immersion Cooling Screening

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

## Fin Efficiency Equation

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

## Representative Fluid Properties Used

The fluid properties are representative screening values and are not tied to one exact commercial product.

| Fluid | Density [kg/m³] | cp [J/kgK] | Dynamic viscosity [Pa·s] | Thermal conductivity [W/mK] | Reference status |
|---|---:|---:|---:|---:|---|
| Air | 1.20 | 1006 | 1.85e-5 | 0.026 | Representative near-room-temperature air properties |
| Water-like coolant | 997 | 4180 | 8.90e-4 | 0.60 | Representative near-room-temperature water properties |
| Representative dielectric liquid | 1400 | 1500 | 4.00e-3 | 0.12 | Representative dielectric-fluid screening assumption |

The air and water-like coolant values are standard near-room-temperature engineering-property values. For a more formal version, these should be checked against NIST or another standard thermophysical-property database at the selected reference temperature.

The dielectric-liquid values are intentionally labelled as representative assumptions. Real immersion fluids vary by product family and temperature. Vendor data for single-phase immersion fluids show that density, viscosity, heat capacity, and thermal conductivity are product-dependent, so a later detailed model should replace the representative values with a specific coolant datasheet.

---

## Bibliography / Sources to Cite

The following sources support the equations, correlations, and property assumptions used in this project.

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

---

## Reference Caveat

The correlations used in this project are standard screening-level heat-transfer correlations. They are appropriate for first-pass engineering estimates, but they do not replace detailed CFD, product-specific coolant data, pressure-drop modelling, or experimental validation.
