# Mechanical and Thermal Design Workflow for a 250 W PCIe AI Accelerator Card

## Project Overview

This project develops a simplified mechanical and thermal design workflow for a high-power PCIe-style AI accelerator card. The goal is to demonstrate practical board-level electronics cooling judgement for accelerator-card applications.

The project includes first-order thermal resistance sizing, PCIe-style mechanical layout, heatsink and airflow planning, CFD boundary-condition definition, TIM and airflow sensitivity studies, first-pass conjugate heat-transfer CFD, and a simulation-to-test validation plan.

This is an original engineering demonstrator. It is not a reverse-engineered commercial accelerator card and does not claim production qualification.

## Engineering Motivation

Modern AI accelerator cards can dissipate high chip-level power and require careful mechanical and thermal design. A useful cooling design must answer several practical engineering questions:

- Does the card fit within the intended PCIe-style mechanical envelope?
- Is the main accelerator chip properly covered by the heatsink base?
- Are memory and VRM components placed with reasonable clearance?
- Is the heatsink fin direction aligned with the expected airflow?
- Can the chip temperature target be met with forced-air cooling?
- How sensitive is the design to TIM thickness, TIM conductivity, and airflow rate?
- How does airflow bypass affect a lower-height heatsink?
- How would the simulation be validated against physical thermal testing?

The purpose of this project is to show the workflow behind these decisions, not only the final simulation result.

## Baseline Product Definition

The demonstrator represents a simplified standard-height, half-length PCIe add-in card.

| Item | Value |
|---|---:|
| Card length | 167.65 mm |
| Card height | 111.15 mm |
| PCB thickness | 1.6 mm |
| Main AI accelerator chip | 45 mm × 45 mm × 2 mm |
| TIM layer | 45 mm × 45 mm × 0.2 mm |
| Baseline heatsink base | 80 mm × 80 mm × 5 mm |
| Baseline fin height | 25 mm |
| Fin thickness | 1 mm |
| Fin spacing | 2 mm |
| Memory chips | 8 blocks around main chip |
| Memory chip size | 14 mm × 12 mm × 1.5 mm |
| VRM region | 60 mm × 15 mm × 3 mm |

The PCIe card envelope is based on publicly available standard-height, half-length PCIe add-in-card references. The chip, heatsink, memory, VRM, TIM, and mounting details are engineering assumptions selected for a realistic portfolio demonstrator.

## Baseline Heat Loads

| Heat Source | Power |
|---|---:|
| Main AI accelerator chip | 250 W |
| Memory chips | 8 × 5 W = 40 W |
| VRM / power delivery region | 30 W |
| Total board heat load | 320 W |

The 250 W chip load represents a high-TDP accelerator-class cooling problem.

## Thermal Design Target

| Quantity | Value |
|---|---:|
| Ambient inlet air temperature | 25 °C |
| Target maximum chip case temperature | 85 °C |
| Allowed chip temperature rise | 60 °C |
| Required chip-to-air thermal resistance | 0.24 K/W |

The required chip-to-air thermal resistance is:

    R_required = (T_chip,max - T_air,inlet) / Q_chip

    R_required = (85 - 25) / 250

    R_required = 0.24 K/W

## Design Evolution

The initial baseline heatsink geometry was defined as an 80 mm × 80 mm × 25 mm aluminum finned heatsink. This compact geometry was used as the starting point for first-order thermal resistance and airflow calculations.

Analytical screening showed that the compact baseline heatsink was not sufficient for the 250 W chip load under realistic forced-air assumptions. The design was therefore expanded to a larger forced-air heatsink candidate for the first CFD stage.

The selected CFD-0 reference candidate used:

| Item | Value |
|---|---:|
| Heatsink base | 80 mm × 100 mm × 5 mm |
| Fin height | 50 mm |
| Fin thickness | 1 mm |
| Fin spacing | 2 mm |
| Number of fins | 26 |
| Guided inlet air velocity | 5 m/s |
| Chip heat load | 250 W |

This larger heatsink candidate was selected because the analytical model predicted that it could meet the 85 °C chip-temperature target with reasonable pressure drop under guided airflow.

After the larger reference case was completed, a lower-height 35 mm heatsink concept was investigated through additional CFD design iterations. The aim was to check whether a more mechanically attractive reduced-height heatsink could also meet the same thermal target when airflow bypass was controlled.

## First-Pass CFD Reference Result

A first-pass conjugate heat-transfer CFD model was completed for the selected larger forced-air heatsink candidate.

The CFD model used a 250 W chip heat load, a 0.2 mm TIM layer, an aluminum heatsink base, 26 fins, and 5 m/s guided inlet airflow.

| Quantity | CFD-0 Result |
|---|---:|
| Maximum chip temperature | 75.97 °C |
| Average chip temperature | 72.00 °C |
| Outlet mass-weighted temperature | 31.86 °C |
| Pressure drop | 28.8 Pa |
| Heat removed by air | approximately 248 W |
| Energy balance error | approximately 0.9% |

The CFD-0 result supports the analytical screening conclusion that the larger forced-air heatsink concept can keep the 250 W chip below the 85 °C target under the assumed 5 m/s guided airflow condition.

Detailed analytical screening is documented here:

[Analytical Screening Summary](docs/analytical_screening_summary.md)

Detailed CFD-0 results are documented here:

[CFD-0 Results](docs/cfd_0_results.md)

## Analytical vs CFD Comparison

| Quantity | Analytical Estimate | CFD-0 Result |
|---|---:|---:|
| Maximum / representative chip temperature | approximately 82.4 °C | approximately 76.0 °C |
| Pressure drop | approximately 30 Pa | approximately 28.8 Pa |

The CFD chip temperature is lower than the analytical estimate by approximately 6.4 °C. This is acceptable for a first-pass comparison because the analytical model was intentionally simplified and conservative.

The pressure-drop agreement is strong, with the CFD result close to the analytical estimate.

The analytical screening workflow is summarized here:

[Analytical Screening Summary](docs/analytical_screening_summary.md)

## CFD-0 Limitations

This CFD result is a stable first coarse CFD result, not a final mesh-independent industrial validation.

Current limitations include:

- coarse first-pass mesh
- no mesh-independence study yet
- laminar first-pass flow assumption
- mild reversed flow at the pressure outlet, affecting approximately 5% of the outlet area
- simplified material properties
- simplified air-domain and boundary-condition representation

Recommended next refinements include extending the outlet region, refining the mesh in the fin channels and solid-fluid interfaces, checking turbulence-model sensitivity, and performing mesh-independence checks.

## CFD Design Iteration

After the larger 80 mm × 100 mm × 50 mm CFD-0 reference case, a second CFD sequence was performed to investigate whether a lower-height 35 mm heatsink concept could meet the same 85 °C chip-temperature target.

A sequence of first-pass CFD simulations was used to evaluate and improve the reduced-height heatsink concept.

| Case | Geometry | Domain | Maximum chip temperature | Pressure drop | Result |
|---|---|---|---:|---:|---|
| CFD-1 | 80 × 100 × 35 mm | Open/bypass | 91.47 °C | 12.7 Pa | Fail |
| CFD-2 | 80 × 100 × 35 mm | Ducted | 87.78 °C | 44.54 Pa | Slight fail |
| CFD-3 | 80 × 120 × 35 mm | Ducted | 83.52 °C | 49.02 Pa | Pass |

The CFD sequence showed that the reduced-height 35 mm heatsink failed in an open/bypass domain because a significant portion of the airflow bypassed the fin region. Adding a ducted airflow path reduced bypass and improved cooling, but the 100 mm long heatsink remained slightly above the 85 °C chip-temperature target.

Extending the ducted heatsink length from 100 mm to 120 mm recovered the remaining thermal margin. The final CFD-3 case reached a maximum chip temperature of 83.52 °C with a pressure drop of approximately 49.02 Pa and a heat-balance error of approximately 0.36%.

Detailed CFD design-iteration documentation:

- [CFD-2 results](docs/cfd_2_results.md)
- [CFD-3 results](docs/cfd_3_results.md)
- [CFD design iteration summary](docs/cfd_design_iteration_summary.md)
- [Final project summary](docs/final_project_summary.md)

## CFD Design Iteration Interpretation

The CFD design iteration produced three important engineering lessons.

First, the open-domain reduced-height heatsink did not fail only because of heatsink size. It also failed because the airflow was not well guided through the fin region. CFD-1 had a relatively low pressure drop of approximately 12.7 Pa and a high maximum chip temperature of 91.47 °C, indicating significant bypass.

Second, ducting improved the reduced-height heatsink. CFD-2 increased the pressure drop to approximately 44.54 Pa and reduced the maximum chip temperature to 87.78 °C. This showed that bypass control was thermally beneficial, but the 100 mm long heatsink still did not provide enough heat-transfer area.

Third, extending the ducted heatsink from 100 mm to 120 mm recovered the remaining thermal margin. CFD-3 reduced the maximum chip temperature to 83.52 °C, which is approximately 1.48 °C below the 85 °C target.

This sequence demonstrates a physics-based design workflow: identify the failure, diagnose the airflow limitation, improve the ducting, and then modify the heatsink geometry to recover thermal margin.

## Project Structure

```text
pcie-ai-accelerator-thermal-design/
├── README.md
├── docs/
│   ├── assumptions.md
│   ├── references.md
│   ├── design_specification.md
│   ├── airflow_sanity_check.md
│   ├── cooling_architecture_tradeoff.md
│   ├── selected_cfd_case.md
│   ├── mechanical_feasibility_check.md
│   ├── pre_cfd_readiness_checklist.md
│   ├── cfd_0_build_steps.md
│   ├── cfd_0_results.md
│   ├── cfd_2_results.md
│   ├── cfd_3_results.md
│   └── cfd_design_iteration_summary.md
├── python/
│   ├── thermal_resistance_model.py
│   ├── tim_sensitivity.py
│   ├── airflow_heat_capacity_check.py
│   ├── heatsink_analytical_model.py
│   ├── heatsink_design_sweep.py
│   ├── passive_fanless_heatsink_model.py
│   └── vapor_chamber_spreading_model.py
├── results/
│   ├── tim_sensitivity.csv
│   ├── airflow_heat_capacity_check.csv
│   ├── heatsink_analytical_model.csv
│   ├── heatsink_design_sweep_full.csv
│   ├── heatsink_design_sweep_passing.csv
│   ├── heatsink_design_sweep_robust_pass_both.csv
│   ├── passive_fanless_heatsink_model.csv
│   └── vapor_chamber_spreading_model.csv
├── figures/
│   ├── baseline_tchip_vs_velocity.png
│   ├── baseline_rhs_vs_velocity.png
│   ├── robust_cfm_vs_tchip.png
│   ├── robust_margin_vs_cfm.png
│   ├── top_robust_candidates_tchip.png
│   └── recommended_candidate_location.png
└── cfd/
    ├── cfd_0_chip_tim_heatsink/
    │   ├── README.md
    │   ├── results/
    │   │   ├── cfd_0_stable_700iter.cas.h5
    │   │   └── cfd_0_stable_700iter.dat.h5
    │   └── screenshots/
    │       ├── temperature_midplane_stable_700iter.png
    │       ├── temperature_isometric_stable_700iter.png
    │       ├── velocity_midplane_stable_700iter.png
    │       └── pressure_midplane_stable_700iter.png
    │
    ├── cfd_2_80x100x35_ducted_domain/
    │   ├── README.md
    │   └── screenshots/
    │       ├── cfd_2_temperature_center_x_plane.png
    │       ├── cfd_2_static_pressure_center_x_plane.png
    │       └── cfd_2_z_velocity_before_fin_plane.png
    │
    └── cfd_3_80x120x35_ducted_domain/
        ├── README.md
        └── screenshots/
            ├── cfd_3_temperature_center_x_plane.png
            ├── cfd_3_static_pressure_center_x_plane.png
            └── cfd_3_z_velocity_fin_entrance_plane.png
```

The `docs/cfd_0_results.md` file contains the detailed first-pass CFD-0 reference result summary, heat balance, convergence assessment, limitations, and contour images.

The `docs/cfd_2_results.md`, `docs/cfd_3_results.md`, and `docs/cfd_design_iteration_summary.md` files document the reduced-height heatsink CFD design iteration.

## Current Engineering Conclusion

The project demonstrates a complete early-stage thermal design workflow:

1. define the PCIe-style board and heat loads
2. calculate the required chip-to-air thermal resistance
3. screen TIM and airflow sensitivity
4. reject compact and passive cooling options
5. select a larger forced-air heatsink reference candidate
6. build first-pass conjugate heat-transfer CFD models
7. diagnose airflow bypass in a reduced-height heatsink design
8. improve cooling through ducting and heatsink length iteration
9. check chip temperature, pressure drop, mass balance, and energy balance
10. document limitations and next refinement steps

The larger 80 mm × 100 mm × 50 mm forced-air heatsink reference case met the 85 °C chip-temperature target with a maximum chip temperature of approximately 75.97 °C.

A reduced-height 35 mm heatsink concept was then investigated through CFD design iteration. The open/bypass 80 mm × 100 mm × 35 mm case failed because of airflow bypass. A ducted version improved the maximum chip temperature from 91.47 °C to 87.78 °C, but still remained slightly above the target. Extending the ducted heatsink length to 120 mm produced a passing result with a maximum chip temperature of 83.52 °C and a pressure drop of approximately 49.02 Pa.

The final CFD-3 result supports the design direction that a ducted 80 mm × 120 mm × 35 mm aluminium heatsink can meet the simplified 250 W chip cooling target in this first-pass thermal feasibility model.

This remains a portfolio-level engineering demonstrator and would require mesh sensitivity, turbulence or transition assessment, mechanical support checks, detailed PCB layout checks, and experimental correlation before being treated as a validated product design.
