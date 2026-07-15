# Uncertainty and DOE Plan for 250 W PCIe AI Accelerator Cooling Concept

## Purpose

This document defines a design-of-experiments and uncertainty-analysis plan for the 250 W PCIe AI accelerator cooling concept.

The current project has completed first-principles thermal screening, heatsink tradeoff analysis, mechanical feasibility planning, a system-level CFD extension plan, and a first-pass ANSYS Fluent conjugate heat-transfer CFD model.

The next step is to define how the design should be tested across uncertain operating and modelling conditions. This is important because a single CFD result is not enough to prove cooling robustness.

## Engineering Context

The current Phase 1 CFD result is based on:

| Parameter | Value |
|---|---:|
| Chip heat load | 250 W |
| Target chip temperature | 85 °C |
| Inlet air temperature | 25 °C |
| Assumed guided inlet velocity | 5 m/s |
| Heatsink footprint | 80 mm × 100 mm |
| Fin height | 50 mm |
| TIM thickness | 0.2 mm |
| TIM conductivity | 6 W/mK |
| CFD maximum chip temperature | approximately 76 °C |
| CFD pressure drop | approximately 28.8 Pa |

This result gives useful first-phase evidence, but the real design margin depends on uncertainties in power, airflow, ambient temperature, TIM condition, geometry, measurement accuracy, and CFD assumptions.

## Why Uncertainty Analysis Is Needed

The cooling result is sensitive to several factors:

- Actual chip power may be higher than nominal.
- Actual airflow through the heatsink may be lower than assumed.
- Chassis or enclosure effects may cause bypass flow.
- TIM thickness and contact resistance may vary during assembly.
- Inlet air temperature may be higher than 25 °C.
- Material properties may differ from assumed values.
- Mesh resolution and turbulence model choice may affect CFD results.
- Measurement uncertainty may affect validation conclusions.

Therefore, the cooling design should be judged using a range of cases, not only one nominal case.

## Main Design Question

The main design question is:

Can the cooling concept keep the chip below 85 °C under realistic uncertainty in power, airflow, ambient temperature, TIM condition, and mechanical geometry?

## Key Uncertain Parameters

| Parameter | Nominal value | Low value | High value | Why it matters |
|---|---:|---:|---:|---|
| Chip power | 250 W | 200 W | 300 W | AI accelerator workload and power limit variation |
| Inlet air velocity | 5 m/s | 3 m/s | 7 m/s | Fan performance and chassis flow distribution |
| Inlet air temperature | 25 °C | 25 °C | 45 °C | Warm enclosure or server inlet condition |
| TIM conductivity | 6 W/mK | 3 W/mK | 8 W/mK | Material selection and ageing |
| TIM thickness | 0.2 mm | 0.1 mm | 0.5 mm | Mounting pressure and assembly variation |
| Fin height | 50 mm | 25 mm | 50 mm | Mechanical envelope constraint |
| Heatsink length | 100 mm | 80 mm | 120 mm | Board-space constraint |
| Flow bypass fraction | 0% ideal | 20% | 50% | Air not passing through fin channels |
| Contact resistance | idealised | low | high | Interface quality and mounting load |

## DOE Strategy

The full parameter space is large. A complete full-factorial study would require too many CFD or test cases.

Therefore, the project should use a staged DOE strategy:

1. One-factor-at-a-time sensitivity for first understanding.
2. Compact screening DOE to identify dominant parameters.
3. Focused CFD cases around the most important risks.
4. Validation tests for the highest-risk and nominal cases.
5. Final design recommendation based on thermal margin and robustness.

## Stage 1: One-Factor Sensitivity Study

The first stage changes one parameter at a time while keeping the others at nominal values.

### Nominal Reference Case

| Parameter | Value |
|---|---:|
| Chip power | 250 W |
| Inlet air velocity | 5 m/s |
| Inlet air temperature | 25 °C |
| TIM conductivity | 6 W/mK |
| TIM thickness | 0.2 mm |
| Fin height | 50 mm |
| Heatsink length | 100 mm |

### Power Sensitivity

| Case | Chip power |
|---|---:|
| P1 | 200 W |
| P2 | 250 W |
| P3 | 300 W |

Purpose: determine chip temperature sensitivity to heat load.

### Airflow Sensitivity

| Case | Inlet air velocity |
|---|---:|
| A1 | 3 m/s |
| A2 | 5 m/s |
| A3 | 7 m/s |

Purpose: determine minimum airflow required to meet the 85 °C target.

### Ambient Temperature Sensitivity

| Case | Inlet air temperature |
|---|---:|
| T1 | 25 °C |
| T2 | 35 °C |
| T3 | 45 °C |

Purpose: evaluate thermal margin under warmer inlet conditions.

### TIM Conductivity Sensitivity

| Case | TIM conductivity |
|---|---:|
| K1 | 3 W/mK |
| K2 | 6 W/mK |
| K3 | 8 W/mK |

Purpose: evaluate sensitivity to TIM material quality.

### TIM Thickness Sensitivity

| Case | TIM thickness |
|---|---:|
| BLT1 | 0.1 mm |
| BLT2 | 0.2 mm |
| BLT3 | 0.5 mm |

Purpose: evaluate sensitivity to bondline thickness and mounting control.

### Fin Height Sensitivity

| Case | Fin height |
|---|---:|
| H1 | 25 mm |
| H2 | 35 mm |
| H3 | 50 mm |

Purpose: connect thermal performance with mechanical envelope constraints.

## Stage 2: Compact DOE Matrix

After one-factor sensitivity, use a compact DOE matrix to combine the most important variables.

Recommended variables for compact DOE:

| Factor | Low | Nominal | High |
|---|---:|---:|---:|
| Chip power | 200 W | 250 W | 300 W |
| Air velocity | 3 m/s | 5 m/s | 7 m/s |
| Inlet temperature | 25 °C | 35 °C | 45 °C |
| TIM condition | Good | Nominal | Poor |
| Fin height | 25 mm | 35 mm | 50 mm |

A complete 3-level full-factorial study would require 3^5 = 243 cases, which is too many for first-pass CFD.

A practical reduced DOE can use 9 to 15 cases.

## Recommended 12-Case DOE Matrix

| Case | Power | Air velocity | Inlet temperature | TIM condition | Fin height | Purpose |
|---|---:|---:|---:|---|---:|---|
| DOE-01 | 250 W | 5 m/s | 25 °C | Nominal | 50 mm | Current reference |
| DOE-02 | 300 W | 5 m/s | 25 °C | Nominal | 50 mm | High power |
| DOE-03 | 250 W | 3 m/s | 25 °C | Nominal | 50 mm | Low airflow |
| DOE-04 | 250 W | 5 m/s | 45 °C | Nominal | 50 mm | High ambient |
| DOE-05 | 250 W | 5 m/s | 25 °C | Poor | 50 mm | Poor TIM |
| DOE-06 | 250 W | 5 m/s | 25 °C | Nominal | 35 mm | Reduced height |
| DOE-07 | 300 W | 3 m/s | 35 °C | Nominal | 35 mm | Combined thermal stress |
| DOE-08 | 300 W | 5 m/s | 45 °C | Poor | 35 mm | Worst practical thermal case |
| DOE-09 | 200 W | 7 m/s | 25 °C | Good | 35 mm | Best practical case |
| DOE-10 | 250 W | 7 m/s | 35 °C | Nominal | 25 mm | Compact high-flow case |
| DOE-11 | 300 W | 7 m/s | 35 °C | Nominal | 35 mm | High power with improved airflow |
| DOE-12 | 250 W | 5 m/s | 35 °C | Poor | 25 mm | Compact poor-interface case |

## TIM Condition Definitions

| TIM condition | Conductivity | Thickness | Meaning |
|---|---:|---:|---|
| Good | 8 W/mK | 0.1 mm | High-performance material and controlled bondline |
| Nominal | 6 W/mK | 0.2 mm | Current design assumption |
| Poor | 3 W/mK | 0.5 mm | Degraded or poorly controlled interface |

This simplified grouping keeps the DOE manageable.

## CFD Output Metrics

For each DOE case, extract:

| Output | Why it matters |
|---|---|
| Maximum chip temperature | Main pass/fail criterion |
| Average chip temperature | Thermal distribution check |
| Maximum memory temperature | Board-level risk |
| Maximum VRM temperature | Power-delivery risk |
| Outlet air temperature | Heat-removal check |
| Mass flow rate | Flow consistency |
| Pressure drop | Fan/system compatibility |
| Heat balance error | Numerical/energy consistency |
| Flow bypass fraction | System airflow effectiveness |
| Maximum heatsink base temperature | Interface and spreading assessment |

## Thermal Margin Calculation

Use the following margin definition:

`Thermal margin = T_target - T_chip,max`

Where:

- T_target = 85 °C
- T_chip,max = maximum predicted or measured chip temperature

Interpretation:

| Thermal margin | Interpretation |
|---|---|
| More than 10 °C | Strong margin |
| 5 to 10 °C | Acceptable first-pass margin |
| 0 to 5 °C | Marginal, needs refinement |
| Less than 0 °C | Fails target |

## Pass/Fail Criteria

| Criterion | Target |
|---|---:|
| Maximum chip temperature | Less than 85 °C |
| Thermal margin | Preferably greater than 5 °C |
| Heat balance error | Less than 5% for first-pass CFD |
| Mass imbalance | Less than 1% |
| Pressure drop | Report and compare with airflow source |
| Stable monitor values | Temperature and pressure should be stable |
| No severe reversed flow | Extend outlet or improve domain if severe |

## Measurement Uncertainty Plan

For validation tests, uncertainty should be estimated for key measured values.

| Measurement | Main uncertainty source |
|---|---|
| Heater power | Voltage and current measurement accuracy |
| Thermocouple temperature | Sensor tolerance and placement |
| Inlet air temperature | Sensor location and flow non-uniformity |
| Outlet air temperature | Mixing and sensor placement |
| Air velocity | Probe accuracy and flow profile |
| Pressure drop | Sensor range and tubing placement |
| TIM thickness | Assembly variation |
| Mounting pressure | Fastener preload variation |

## Example Measurement Uncertainty Table

| Quantity | Estimated uncertainty | Comment |
|---|---:|---|
| Heater power | ±2–5% | Depends on power-supply and measurement method |
| Thermocouple temperature | ±1–2 °C | Depends on sensor class and attachment |
| Air velocity | ±5–10% | Depends on probe and flow uniformity |
| Pressure drop | ±5–10% | Depends on differential pressure sensor |
| TIM bondline thickness | ±25–50% | Can vary strongly without controlled mounting |

These values are first-pass engineering estimates and should be replaced by actual instrument specifications when available.

## CFD Uncertainty Plan

CFD uncertainty should be assessed using:

| Uncertainty source | Check |
|---|---|
| Mesh resolution | Coarse, medium, refined mesh comparison |
| Turbulence model | Laminar versus k-omega SST for system-level model |
| Boundary condition | Velocity inlet versus mass-flow inlet |
| Outlet placement | Longer downstream extension |
| Material properties | Conductivity sensitivity |
| Contact/interface assumption | TIM resistance sensitivity |
| Heat-source distribution | Uniform versus local heat generation |
| Enclosure size | Chamber dimension sensitivity |

At least one representative case should be repeated with a finer mesh to confirm that design conclusions are not mesh-dependent.

## Recommended Mesh-Check Case

Use the nominal reference system case:

| Parameter | Value |
|---|---:|
| Power | 250 W |
| Air velocity | 5 m/s |
| Inlet temperature | 25 °C |
| TIM | Nominal |
| Heatsink | 80 × 100 × 35 or 50 mm |

Run:

| Mesh | Purpose |
|---|---|
| Coarse | Fast trend check |
| Medium | Main engineering result |
| Refined | Mesh-dependence check |

Compare:

- Maximum chip temperature
- Pressure drop
- Outlet temperature
- Heat balance error
- Velocity pattern through fins

## DOE Result Table Template

Use this table format for reporting DOE results:

| Case | Power | Airflow | Inlet T | TIM | Fin height | Tmax chip | Margin | Pressure drop | Heat balance error | Result |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|
| DOE-01 | 250 W | 5 m/s | 25 °C | Nominal | 50 mm | TBD | TBD | TBD | TBD | TBD |
| DOE-02 | 300 W | 5 m/s | 25 °C | Nominal | 50 mm | TBD | TBD | TBD | TBD | TBD |
| DOE-03 | 250 W | 3 m/s | 25 °C | Nominal | 50 mm | TBD | TBD | TBD | TBD | TBD |

## Decision Logic

After DOE and uncertainty analysis, classify the cooling concept as:

| Classification | Meaning |
|---|---|
| Robust pass | Passes target with margin across most realistic cases |
| Conditional pass | Passes only with sufficient airflow, ducting, or controlled TIM |
| Marginal | Passes nominal case but fails important sensitivity cases |
| Fail | Cannot meet 85 °C target under realistic constraints |

The current Phase 1 result should be considered a nominal-case pass, not a robust product-level pass.

## Expected Engineering Interpretation

Possible outcomes:

| Observation | Interpretation |
|---|---|
| Temperature strongly depends on airflow | Fan/ducting is dominant design risk |
| Temperature strongly depends on TIM | Mounting pressure and interface control are critical |
| Reduced-height heatsink fails | Mechanical envelope creates thermal challenge |
| High ambient causes failure | Need lower thermal resistance or lower power limit |
| Pressure drop increases strongly with ducting | Fan operating point must be checked |
| CFD and test differ by more than 10 °C | Model assumptions or measurements require investigation |

## Link to Validation Plan

The DOE should guide the physical validation plan.

Not every DOE case needs to be tested physically. The most important test cases are:

1. Nominal reference case.
2. High-power case.
3. Low-airflow case.
4. Reduced-height heatsink case.
5. Poor-TIM or remounting case.
6. High-ambient case if chamber access exists.

These cases provide useful simulation-to-test correlation without requiring an excessive number of experiments.

## Link to Mechanical Feasibility

Mechanical constraints may reduce fin height, limit heatsink footprint, or require a different mounting method. Therefore, the DOE should include mechanically realistic variants, not only the thermally best variant.

The 80 mm × 100 mm × 50 mm heatsink remains useful as a Phase 1 thermal reference. However, reduced-height variants such as 35 mm and 25 mm are important for mechanical feasibility.

## Limitations

This DOE and uncertainty plan is a first-pass engineering framework. It does not include:

- Formal statistical DOE optimisation
- Full factorial testing
- Reliability qualification
- Manufacturing tolerance stack-up
- Detailed package thermal model uncertainty
- Fan-curve uncertainty unless fan data is available
- Long-duration thermal cycling
- Production acceptance criteria

The purpose is to make the next simulation and validation steps structured, traceable, and defensible.

## Summary

The first-pass CFD result showed that the selected forced-air heatsink concept can cool the 250 W chip under idealised guided-airflow assumptions. However, a single nominal CFD result is not enough to judge product readiness.

This uncertainty and DOE plan defines how to test the design against realistic variations in chip power, airflow, inlet temperature, TIM condition, and mechanical geometry.

The main goal is to determine whether the cooling concept is a robust pass, conditional pass, marginal design, or fail under realistic operating and integration constraints.