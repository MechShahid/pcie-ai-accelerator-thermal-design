# Validation Plan for 250 W PCIe AI Accelerator Cooling Concept

## Purpose

This document defines a practical validation plan for the 250 W PCIe AI accelerator cooling concept.

The current project has completed first-principles thermal screening, heatsink tradeoff analysis, and a first-pass ANSYS Fluent conjugate heat-transfer CFD model. However, the current CFD result is not a final validated product prediction. A physical validation plan is required to compare simulation results with measured thermal and airflow behaviour.

The aim of this document is to define how the cooling concept could be tested, measured, and correlated with CFD in a controlled laboratory setup.

## Validation Objectives

The validation campaign should answer the following engineering questions:

1. Can the cooling solution keep the chip or chip surrogate below the 85 °C target?
2. How closely do measured temperatures match CFD predictions?
3. Is the assumed airflow through the heatsink achievable in a realistic setup?
4. What is the pressure drop across the heatsink or cooling path?
5. How much heat is removed by the air stream?
6. How sensitive is the result to airflow, input power, ambient temperature, and TIM condition?
7. Does the cooling concept remain acceptable when neighbouring board heat sources are included?

## Current CFD Reference Case

The current Phase 1 CFD reference case is:

| Parameter | Value |
|---|---:|
| Chip heat load | 250 W |
| Chip size | 45 mm × 45 mm |
| TIM thickness | 0.2 mm |
| TIM conductivity | 6 W/mK |
| Heatsink footprint | 80 mm × 100 mm |
| Fin height | 50 mm |
| Inlet air temperature | 25 °C |
| Assumed inlet velocity | 5 m/s |
| CFD maximum chip temperature | approximately 76 °C |
| CFD pressure drop | approximately 28.8 Pa |
| CFD heat-balance error | below 1% |

This case should be treated as the first simulation reference for test correlation.

## Proposed Test Article

A practical first validation setup can use a simplified heater-block test article rather than a full functional AI accelerator card.

### Test Article Components

| Component | Purpose |
|---|---|
| Copper or aluminium heater block | Represents chip thermal footprint |
| Cartridge heaters or electrical heater pad | Provides controlled heat input |
| Thermocouples in heater block | Estimate chip-case or heater temperature |
| TIM layer | Represents interface between chip and heatsink |
| Heatsink prototype | Cooling solution under test |
| Insulation around heater block | Reduce parasitic heat loss |
| Simple board plate | Represents approximate mounting and airflow blockage |
| Optional memory/VRM heater blocks | Represent neighbouring board heat loads |

The heater block should have a similar footprint to the modelled chip, approximately 45 mm × 45 mm.

## Instrumentation Plan

### Temperature Measurements

Recommended measurement locations:

| Measurement point | Purpose |
|---|---|
| Heater block centre | Main chip surrogate temperature |
| Heater block corner | Check temperature uniformity |
| Heatsink base near chip | Check TIM/base temperature rise |
| Fin inlet air | Confirm inlet temperature |
| Fin outlet air | Estimate air temperature rise |
| Ambient chamber air | Monitor test environment |
| Optional memory block | Board-level temperature check |
| Optional VRM block | Power-stage temperature check |

Use multiple thermocouples because a single point measurement is not enough to understand thermal gradients.

### Airflow Measurements

Recommended measurements:

| Measurement | Purpose |
|---|---|
| Inlet air velocity | Check imposed airflow |
| Outlet air velocity | Check flow development |
| Volumetric flow rate | Estimate total cooling airflow |
| Mass flow rate | Calculate air-side heat removal |
| Flow uniformity | Check whether fins receive uniform flow |

Possible tools:

- Hot-wire anemometer
- Vane anemometer
- Flow hood
- Calibrated duct measurement
- Fan curve and pressure measurement

### Pressure Measurements

Recommended measurements:

| Measurement | Purpose |
|---|---|
| Static pressure before heatsink | Upstream reference |
| Static pressure after heatsink | Downstream reference |
| Pressure drop across heatsink | Compare with CFD |
| Pressure drop across full duct/chamber | Check system impedance |

A differential pressure sensor or manometer can be used.

### Power Measurements

Recommended measurements:

| Measurement | Purpose |
|---|---|
| Heater voltage | Electrical input |
| Heater current | Electrical input |
| Electrical power | Thermal power estimate |
| Power stability | Check steady-state condition |

Electrical power should be calculated from measured voltage and current, not only from the power-supply setting.

## Test Matrix

A first validation campaign should be small but structured.

### Power Sweep

| Case | Chip surrogate power |
|---|---:|
| P1 | 150 W |
| P2 | 200 W |
| P3 | 250 W |
| P4 | 300 W |

Purpose: check whether the model scales correctly with heat load.

### Airflow Sweep

| Case | Air velocity |
|---|---:|
| A1 | 3 m/s |
| A2 | 5 m/s |
| A3 | 7 m/s |

Purpose: check sensitivity to airflow and determine minimum acceptable airflow.

### Ambient Temperature Sweep

| Case | Inlet air temperature |
|---|---:|
| T1 | 25 °C |
| T2 | 35 °C |
| T3 | 45 °C |

Purpose: check thermal margin under warmer operating conditions.

### TIM Sensitivity

| Case | TIM condition |
|---|---|
| TIM1 | Nominal TIM bondline |
| TIM2 | Thicker TIM bondline |
| TIM3 | Lower-conductivity TIM |
| TIM4 | Re-mounted TIM after assembly |

Purpose: understand sensitivity to assembly and interface quality.

## Minimum Recommended First Test Set

If lab time is limited, start with:

| Test | Power | Airflow | Inlet temperature |
|---|---:|---:|---:|
| 1 | 200 W | 5 m/s | 25 °C |
| 2 | 250 W | 5 m/s | 25 °C |
| 3 | 300 W | 5 m/s | 25 °C |
| 4 | 250 W | 3 m/s | 25 °C |
| 5 | 250 W | 7 m/s | 25 °C |
| 6 | 250 W | 5 m/s | 35 °C |

This gives a compact but useful validation set.

## CFD-to-Test Correlation Method

For each test case, compare measured and simulated values.

| Quantity | Simulation | Test | Difference |
|---|---:|---:|---:|
| Maximum chip/heater temperature | CFD value | Measured value | Test - CFD |
| Heatsink base temperature | CFD value | Measured value | Test - CFD |
| Outlet air temperature | CFD value | Measured value | Test - CFD |
| Pressure drop | CFD value | Measured value | Test - CFD |
| Mass flow rate | CFD value | Measured value | Test - CFD |
| Air-side heat removal | CFD value | Measured value | Test - CFD |

A useful correlation metric is:

`Temperature error = T_measured - T_CFD`

For heat removal:

`Q_air = m_dot × cp × (T_out - T_in)`

The air-side heat removal should be compared with electrical input power. Large mismatch indicates heat loss to surroundings, measurement error, or incorrect mass-flow estimate.

## Acceptance Criteria

Suggested first-pass validation criteria:

| Metric | Target |
|---|---:|
| Maximum chip/heater temperature | Below 85 °C at 250 W |
| CFD-to-test chip temperature difference | Within ±10 °C for first correlation |
| Heat balance error | Within ±10% for first lab setup |
| Pressure-drop difference | Within ±20–30% for first setup |
| Repeatability after remounting | Temperature variation recorded and explained |
| Stable steady-state temperature | Less than 0.5 °C change over final 5–10 minutes |

These are first-pass engineering criteria. A production validation plan would require tighter acceptance limits and more formal test controls.

## Uncertainty Sources

Important uncertainty sources include:

| Source | Effect |
|---|---|
| Thermocouple placement | Temperature measurement error |
| Contact resistance | Higher chip temperature |
| TIM bondline variation | Thermal resistance variation |
| Air velocity measurement | Error in heat-removal estimate |
| Non-uniform airflow | Local hotspot and correlation mismatch |
| Heat loss to surroundings | Air-side heat balance error |
| Heater power uncertainty | Input power mismatch |
| Material property uncertainty | CFD prediction uncertainty |
| Mesh and turbulence model choice | Simulation uncertainty |
| Mounting pressure variation | Repeatability issue |

These should be recorded during testing.

## Reporting Template

Each validation case should be reported in the following format:

- Test case ID:
- Heatsink geometry:
- Power input:
- Inlet air temperature:
- Measured airflow:
- Measured pressure drop:
- Maximum measured heater/chip temperature:
- Measured outlet air temperature:
- Calculated air-side heat removal:
- Equivalent CFD case:
- CFD maximum chip temperature:
- CFD outlet air temperature:
- CFD pressure drop:
- Temperature difference:
- Pressure-drop difference:
- Engineering conclusion:

## Example Correlation Table

| Case | Power | Airflow | CFD Tmax | Test Tmax | Difference | Pass/Fail |
|---|---:|---:|---:|---:|---:|---|
| Example | 250 W | 5 m/s | 76 °C | To be measured | To be calculated | TBD |

## Link to Next CFD Phase

The validation plan should be linked to the system-level CFD extension.

The next CFD model should include:

- Board outline
- Memory and VRM heat loads
- Enclosure or duct
- Bypass airflow
- Longer outlet region
- Fan or mass-flow boundary condition
- Reduced-height heatsink variants

The same quantities measured in the lab should be extracted from CFD to make comparison straightforward.

## Limitations

This validation plan is intended for a portfolio-level engineering workflow. It is not yet a certified production qualification plan.

It does not include:

- Full reliability testing
- Vibration and shock testing
- Thermal cycling qualification
- EMC considerations
- Detailed package junction-to-case calibration
- Supplier production tolerances
- Long-duration ageing tests
- Full customer acceptance testing

## Summary

The current CFD result is a useful first-phase thermal prediction, but it requires physical validation before being treated as a reliable product-level result.

A practical heater-block validation setup can test the cooling concept using controlled power input, measured airflow, thermocouples, pressure-drop measurement, and CFD-to-test comparison.

The main goal is to establish whether the cooling concept can keep a 250 W chip surrogate below the 85 °C target and to identify where simulation and measurement differ.