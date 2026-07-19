# Final Project Summary

## Project Title

Mechanical and Thermal Design Workflow for a 250 W PCIe AI Accelerator Card

## Project Purpose

This project demonstrates an early-stage mechanical and thermal design workflow for a simplified high-power PCIe-style AI accelerator card.

The objective was to evaluate whether a 250 W accelerator chip could be cooled below an 85 °C maximum chip-temperature target using forced-air heatsink cooling, while considering heatsink size, airflow delivery, pressure drop, TIM resistance, and mechanical feasibility.

This is a portfolio-level engineering demonstrator. It is not a reverse-engineered commercial product and does not claim production qualification.

## Design Target

| Quantity | Value |
|---|---:|
| Chip heat load | 250 W |
| Inlet air temperature | 25 °C |
| Maximum chip-temperature target | 85 °C |
| Required chip-to-air thermal resistance | 0.24 K/W |
| Cooling approach | Forced-air finned heatsink |

## Workflow

The project followed a staged engineering workflow:

1. Defined a simplified PCIe-style accelerator card geometry.
2. Estimated the required chip-to-air thermal resistance.
3. Performed analytical heatsink and airflow screening.
4. Checked TIM sensitivity and airflow heat-capacity limits.
5. Rejected compact and passive/fanless cooling options.
6. Selected a larger forced-air reference heatsink.
7. Built first-pass conjugate heat-transfer CFD models.
8. Diagnosed airflow bypass in a reduced-height heatsink design.
9. Improved the design using ducting and heatsink length iteration.
10. Documented limitations and future validation requirements.
11. Estimated heatsink mass, weight force, and approximate bending moment.
12. Classified mechanical support risk and recommended support concepts.

## Main CFD Results

| Case | Geometry | Domain | Maximum chip temperature | Pressure drop | Result |
|---|---|---|---:|---:|---|
| CFD-0 | 80 × 100 × 50 mm | Guided/open first-pass | 75.97 °C | 28.8 Pa | Pass |
| CFD-1 | 80 × 100 × 35 mm | Open/bypass | 91.47 °C | 12.7 Pa | Fail |
| CFD-2 | 80 × 100 × 35 mm | Ducted | 87.78 °C | 44.54 Pa | Slight fail |
| CFD-3 | 80 × 120 × 35 mm | Ducted | 83.52 °C | 49.02 Pa | Pass |

## Key Engineering Findings

The larger 80 × 100 × 50 mm reference heatsink passed the thermal target with a maximum chip temperature of approximately 75.97 °C.

The reduced-height 80 × 100 × 35 mm heatsink failed in an open/bypass domain. Although the inlet mass flow rate was high, the low pressure drop and high chip temperature indicated that a significant portion of the airflow bypassed the fin region.

Adding a ducted airflow path improved the reduced-height heatsink performance. The maximum chip temperature decreased from 91.47 °C to 87.78 °C, but the case still remained slightly above the 85 °C target.

Extending the ducted heatsink length from 100 mm to 120 mm recovered the remaining thermal margin. CFD-3 achieved a maximum chip temperature of 83.52 °C with a pressure drop of approximately 49.02 Pa and a heat-balance error of approximately 0.36%.

## Final Design Direction

The final first-pass thermal feasibility candidate is:

| Quantity | Value |
|---|---:|
| Heatsink geometry | 80 × 120 × 35 mm |
| Material | Aluminium |
| Fin count | 26 |
| Fin thickness | 1 mm |
| Fin gap | 2 mm |
| Inlet airflow | 5 m/s ducted flow |
| Chip heat load | 250 W |
| Maximum chip temperature | 83.52 °C |
| Pressure drop | 49.02 Pa |
| Result | Pass |

This result supports the design direction that a ducted 80 × 120 × 35 mm aluminium heatsink can meet the simplified 250 W chip cooling target in the first-pass CFD model.

## Why This Project Is Useful

This project demonstrates more than simply running CFD. It shows a complete engineering reasoning process:

- first-principles thermal resistance estimation
- analytical heatsink screening
- airflow and TIM sensitivity checks
- CFD boundary-condition setup
- failure diagnosis using pressure drop and airflow bypass
- design iteration from failed to passing configuration
- heat-balance and mass-balance checking
- honest documentation of assumptions and limitations

## Mechanical Support Screening

A concept-level mechanical support screening was added after the final CFD-3 thermal candidate was selected.

The final ducted 80 × 120 × 35 mm aluminium heatsink has an estimated mass of approximately 424 g, weight force of approximately 4.16 N, and approximate bending moment of 0.146 N·m using a simplified 35 mm lever-arm assumption.

This places the final heatsink candidate in a high support-risk category. Therefore, the design is thermally feasible but mechanically support-sensitive. A backplate, bracket, standoffs, or chassis-supported duct is recommended before treating the design as mechanically feasible.

## Limitations

This remains a first-pass thermal feasibility study, not final product validation.

Further work would require:

- mesh-sensitivity study
- turbulence or transition model assessment
- fan curve and system-level airflow modelling
- detailed PCB, memory, and VRM heat sources
- mechanical support and mass evaluation
- component keep-out and mounting checks
- experimental thermal validation
- pressure-drop comparison with fan/system capability

## Final Statement

The project demonstrates a physics-based mechanical and thermal design workflow for a simplified PCIe-style AI accelerator card. The final CFD design iteration identified a ducted 80 × 120 × 35 mm aluminium heatsink as a passing first-pass thermal feasibility candidate for a 250 W chip heat load.
