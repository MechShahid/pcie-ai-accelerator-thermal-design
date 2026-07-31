# Final Project Summary

## Project Title

Mechanical and Thermal Design Workflow for a 250 W PCIe AI Accelerator Card

## Project Purpose

This project demonstrates an early-stage mechanical and thermal design workflow for a simplified high-power PCIe-style AI accelerator card.

The objective was to evaluate whether a 250 W accelerator chip could be cooled below an 85 °C maximum chip-temperature target using forced-air heatsink cooling, while considering heatsink size, airflow delivery, pressure drop, TIM resistance, airflow bypass, mesh sensitivity, viscous-model sensitivity, mechanical support risk, and first-pass liquid/immersion cooling alternatives.

This is a portfolio-level engineering demonstrator. It is not a reverse-engineered commercial product and does not claim production qualification.

---

## Design Target

| Quantity | Value |
|---|---:|
| Chip heat load | 250 W |
| Inlet air temperature | 25 °C |
| Maximum chip-temperature target | 85 °C |
| Required chip-to-air thermal resistance | 0.24 K/W |
| Main cooling approach | Forced-air finned heatsink |

The required chip-to-air thermal resistance is:

```text
R_required = (85 - 25) / 250 = 0.24 K/W
```

---

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
10. Performed a refined-mesh repeat of the final ducted CFD case.
11. Added a k-omega SST viscous-model sensitivity case.
12. Checked chip temperature, pressure drop, mass balance, and heat balance.
13. Added concept-level mechanical support screening.
14. Added liquid and immersion cooling screening.
15. Documented assumptions, limitations, and validation requirements.

---

## Main CFD Results

| Case | Geometry | Domain / model | Maximum chip temperature | Pressure drop | Result |
|---|---|---|---:|---:|---|
| CFD-0 | 80 × 100 × 50 mm | Guided/open first-pass, laminar | 75.97 °C | 28.8 Pa | Pass |
| CFD-1 | 80 × 100 × 35 mm | Open/bypass, laminar | 91.47 °C | 12.7 Pa | Fail |
| CFD-2 | 80 × 100 × 35 mm | Ducted, laminar | 87.78 °C | 44.54 Pa | Slight fail |
| CFD-3 | 80 × 120 × 35 mm | Ducted, laminar | 83.52 °C | 49.02 Pa | Pass |
| CFD-4A | 80 × 120 × 35 mm | Ducted, refined mesh, laminar | 78.11 °C | 56.36 Pa | Pass, mesh-sensitivity check |
| CFD-4B | 80 × 120 × 35 mm | Ducted, refined mesh, k-omega SST | 68.50 °C | 83.84 Pa | Pass, turbulence-model sensitivity check |

---

## Key Engineering Findings

The larger 80 × 100 × 50 mm reference heatsink passed the thermal target with a maximum chip temperature of approximately 75.97 °C.

The reduced-height 80 × 100 × 35 mm heatsink failed in an open/bypass domain. Although the inlet mass flow rate was high, the low pressure drop and high chip temperature indicated that a significant portion of the airflow bypassed the fin region.

Adding a ducted airflow path improved the reduced-height heatsink performance. The maximum chip temperature decreased from 91.47 °C to 87.78 °C, but the case still remained slightly above the 85 °C target.

Extending the ducted heatsink length from 100 mm to 120 mm recovered the remaining thermal margin. CFD-3 achieved a maximum chip temperature of 83.52 °C with a pressure drop of approximately 49.02 Pa and a heat-balance error of approximately 0.36%.

A refined-mesh repeat was added as CFD-4A. The refined mesh used approximately 511k elements compared with approximately 188k elements in CFD-3. CFD-4A predicted a maximum chip temperature of 78.11 °C and a pressure drop of 56.36 Pa. This supports the thermal feasibility of the ducted 80 × 120 × 35 mm heatsink, but the approximately 5.4 °C change in maximum chip temperature means the result should be treated as a mesh-sensitivity check rather than full mesh-independent validation.

A k-omega SST case was added as CFD-4B using the same refined mesh. The SST case predicted a lower maximum chip temperature of 68.50 °C and a higher pressure drop of 83.84 Pa. This shows that the final design remains below the 85 °C target under both refined laminar and SST assumptions, but the detailed prediction is sensitive to viscous-model choice.

---

## Final Forced-Air Design Direction

The final forced-air thermal feasibility candidate is:

| Quantity | Value |
|---|---:|
| Heatsink geometry | 80 × 120 × 35 mm |
| Material | Aluminium |
| Fin count | 26 |
| Fin thickness | 1 mm |
| Fin gap | 2 mm |
| Inlet airflow | 5 m/s ducted flow |
| Chip heat load | 250 W |
| CFD-3 maximum chip temperature | 83.52 °C |
| CFD-3 pressure drop | 49.02 Pa |
| CFD-4A refined-mesh maximum chip temperature | 78.11 °C |
| CFD-4B SST maximum chip temperature | 68.50 °C |
| Result | Thermally feasible in first-pass CFD |

This result supports the design direction that a ducted 80 × 120 × 35 mm aluminium heatsink can meet the simplified 250 W chip cooling target in a first-pass thermal feasibility model.

However, CFD-4A and CFD-4B show that the detailed numerical value depends on mesh resolution and viscous-model choice. Therefore, this should not be described as validated product performance.

---

## Mesh and Turbulence Sensitivity

CFD-4A was added to check mesh sensitivity. The refined mesh improved mesh-quality indicators and increased the element count by approximately 2.7×. The design still passed the thermal target, but the maximum chip temperature changed by approximately 5.4 °C compared with CFD-3.

CFD-4B was added to check viscous-model sensitivity. The estimated fin-channel Reynolds number was near the transitional range, so k-omega SST was used only as a sensitivity check, not as proof that the real flow is fully turbulent. The SST model predicted stronger cooling and higher pressure drop than the refined laminar case.

The safe conclusion is:

```text
The final ducted heatsink remains thermally feasible under both refined laminar and k-omega SST assumptions, but further mesh refinement, near-wall checks, transition/turbulence modelling, and experimental correlation would be required before claiming validated CFD accuracy.
```

---

## Mechanical Support Screening

A concept-level mechanical support screening was added after the thermal design iteration.

The final 80 × 120 × 35 mm heatsink has an estimated mass of approximately 424 g and an approximate bending moment of 0.146 N·m using a simplified 35 mm lever-arm assumption.

| Case | Geometry | Estimated mass | Weight force | Approx. bending moment | Support risk |
|---|---|---:|---:|---:|---|
| CFD-0 | 80 × 100 × 50 mm | 459.00 g | 4.50 N | 0.158 N·m | High |
| CFD-1 / CFD-2 | 80 × 100 × 35 mm | 353.70 g | 3.47 N | 0.121 N·m | High |
| CFD-3 | 80 × 120 × 35 mm | 424.44 g | 4.16 N | 0.146 N·m | High |

Therefore, the final forced-air heatsink concept is thermally feasible but mechanically support-sensitive. A backplate, bracket, standoffs, or chassis-supported duct is recommended before treating the design as mechanically feasible.

---

## Liquid and Immersion Cooling Extension

A liquid and immersion cooling screening extension was added to compare the same 250 W chip heat load using first-principles and empirical-correlation estimates.

For a 250 W heat load and 10 K bulk coolant temperature rise, the required volume flow rates were:

| Fluid | Required volume flow |
|---|---:|
| Air | 1242.54 L/min |
| Water-like coolant | 0.360 L/min |
| Representative dielectric liquid | 0.714 L/min |

The main finding is that liquid coolants can carry the same heat load with far lower volumetric flow than air. However, coolant heat-carrying capacity alone does not guarantee low chip temperature. Local heat-transfer coefficient, wetted area, heat spreading, and flow architecture are also critical.

The component-level convective screening gave:

| Case | Estimated surface-to-fluid temperature rise |
|---|---:|
| Direct-to-chip cold plate | 44.95 K |
| Bare immersion flat plate | 927.2 K |
| Spreader-only immersion flat plate | 521.5 K |
| Finned immersion heat spreader | 88.8 K |

This shows why practical immersion cooling requires more than simply exposing the chip footprint to dielectric liquid. Heat spreading and increased wetted area are essential.

---

## Why This Project Is Useful

This project demonstrates more than simply running CFD. It shows a complete engineering reasoning process:

- first-principles thermal resistance estimation
- analytical heatsink screening
- airflow and TIM sensitivity checks
- CFD boundary-condition setup
- failure diagnosis using pressure drop and airflow bypass
- design iteration from failed to passing configuration
- heat-balance and mass-balance checking
- mesh-sensitivity checking
- turbulence-model sensitivity checking
- concept-level mechanical support assessment
- liquid and immersion cooling screening
- honest documentation of assumptions and limitations

---

## Limitations

This remains a first-pass thermal feasibility and portfolio-level design study, not final product validation.

Further work would require:

- additional mesh refinement and local near-wall/interface checks
- transition-model assessment and turbulence-model validation
- fan curve and system-level airflow modelling
- detailed PCB, memory, and VRM heat-source modelling
- component keep-out and mounting checks
- detailed mechanical support design
- PCB structural FEA
- shock and vibration assessment
- liquid-cooling pressure-drop modelling
- immersion-system CFD
- material/contact-resistance refinement
- experimental thermal validation
- pressure-drop comparison with fan/system capability

---

## Final Statement

The project demonstrates a physics-based mechanical and thermal design workflow for a simplified PCIe-style AI accelerator card.

The final CFD design iteration identified a ducted 80 × 120 × 35 mm aluminium heatsink as a passing first-pass thermal feasibility candidate for a 250 W chip heat load. CFD-3 predicted a maximum chip temperature of 83.52 °C, CFD-4A confirmed that the design remained feasible under mesh refinement, and CFD-4B showed that the design also remained below the target under a k-omega SST sensitivity case.

The project also identified an important mechanical support risk due to heatsink mass and bending moment, and it extended the workflow to liquid and immersion cooling screening. Overall, the work demonstrates practical thermal-fluid reasoning, CFD setup and interpretation, design iteration, sensitivity checking, and honest engineering judgement.
