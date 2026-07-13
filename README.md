# Mechanical and Thermal Design Workflow for a 250 W PCIe AI Accelerator Card

## Project Overview

This project develops a simplified mechanical and thermal design workflow for a high-power PCIe-style AI accelerator card. The goal is to demonstrate practical board-level electronics cooling judgement for accelerator-card applications.

The project includes first-order thermal resistance sizing, PCIe-style mechanical layout, heatsink and airflow planning, CFD boundary-condition definition, TIM and airflow sensitivity studies, and a simulation-to-test validation plan.

This is an original engineering demonstrator. It is not a reverse-engineered commercial accelerator card and does not claim production qualification.

## Engineering Motivation

Modern AI accelerator cards can dissipate high chip-level power and require careful mechanical and thermal design. A useful cooling design must answer several practical engineering questions:

- Does the card fit within the intended PCIe-style mechanical envelope?
- Is the main accelerator chip properly covered by the heatsink base?
- Are memory and VRM components placed with reasonable clearance?
- Is the heatsink fin direction aligned with the expected airflow?
- Can the chip temperature target be met with forced-air cooling?
- How sensitive is the design to TIM thickness, TIM conductivity, and airflow rate?
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

```text
R_required = (T_chip,max - T_air,inlet) / Q_chip

R_required = (85 - 25) / 250

R_required = 0.24 K/W
```

## Design Evolution

The initial baseline heatsink geometry was defined as an 80 mm × 80 mm × 25 mm aluminum finned heatsink. This compact geometry was used as the starting point for first-order thermal resistance and airflow calculations.

Analytical screening showed that the compact baseline heatsink was not sufficient for the 250 W chip load under realistic forced-air assumptions. The design was therefore expanded to a larger forced-air heatsink candidate for the CFD stage.

The selected CFD 0 candidate uses:

| Item | Value |
|---|---:|
| Heatsink base | 80 mm × 100 mm × 5 mm |
| Fin height | 50 mm |
| Fin thickness | 1 mm |
| Fin spacing | 2 mm |
| Number of fins | 26 |
| Guided inlet air velocity | 5 m/s |
| Chip heat load | 250 W |

This larger heatsink candidate was selected because the analytical model predicted that it could meet the 85 °C chip temperature target with reasonable pressure drop under guided airflow.

## First-Pass CFD Result

A first-pass conjugate heat-transfer CFD model was completed for the selected larger forced-air heatsink candidate.

The CFD model used a 250 W chip heat load, a 0.2 mm TIM layer, an aluminum heatsink base, 26 fins, and 5 m/s guided inlet airflow.

| Quantity | CFD 0 Result |
|---|---:|
| Maximum chip temperature | 75.97 °C |
| Average chip temperature | 72.00 °C |
| Outlet mass-weighted temperature | 31.86 °C |
| Pressure drop | 28.8 Pa |
| Heat removed by air | approximately 248 W |
| Energy balance error | approximately 0.9% |

The first-pass CFD result supports the analytical screening conclusion that the selected forced-air heatsink concept can keep the 250 W chip below the 85 °C target under the assumed 5 m/s guided airflow condition.

Detailed analytical screening is documented here:

[Analytical Screening Summary](docs/analytical_screening_summary.md)

Detailed CFD results are documented here:

[CFD 0 Results](docs/cfd_0_results.md)

## Analytical vs CFD Comparison

| Quantity | Analytical Estimate | CFD 0 Result |
|---|---:|---:|
| Maximum / representative chip temperature | approximately 82.4 °C | approximately 76.0 °C |
| Pressure drop | approximately 30 Pa | approximately 28.8 Pa |

The CFD chip temperature is lower than the analytical estimate by approximately 6.4 °C. This is acceptable for a first-pass comparison because the analytical model was intentionally simplified and conservative.

The pressure-drop agreement is strong, with the CFD result close to the analytical estimate.

The analytical screening workflow is summarized here:

[Analytical Screening Summary](docs/analytical_screening_summary.md)

## CFD 0 Limitations

This CFD result is a stable first coarse CFD result, not a final mesh-independent industrial validation.

Current limitations include:

- coarse first-pass mesh
- no mesh-independence study yet
- laminar first-pass flow assumption
- mild reversed flow at the pressure outlet, affecting approximately 5% of the outlet area
- simplified material properties
- simplified air-domain and boundary-condition representation

Recommended next refinements include extending the outlet region, refining the mesh in the fin channels and solid-fluid interfaces, checking turbulence-model sensitivity, and performing mesh-independence checks.

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
│   └── cfd_0_results.md
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
    └── cfd_0_chip_tim_heatsink/
        ├── README.md
        ├── results/
        │   ├── cfd_0_stable_700iter.cas.h5
        │   └── cfd_0_stable_700iter.dat.h5
        └── screenshots/
            ├── temperature_midplane_stable_700iter.png
            ├── temperature_isometric_stable_700iter.png
            ├── velocity_midplane_stable_700iter.png
            └── pressure_midplane_stable_700iter.png
```

The `docs/cfd_0_results.md` file contains the detailed first-pass CFD result summary, heat balance, convergence assessment, limitations, and contour images.

## Current Engineering Conclusion

The project demonstrates a complete early-stage thermal design workflow:

1. define the PCIe-style board and heat loads
2. calculate the required chip-to-air thermal resistance
3. screen TIM and airflow sensitivity
4. reject compact and passive cooling options
5. select a larger forced-air heatsink candidate
6. build a first-pass CFD model
7. check chip temperature, pressure drop, mass balance, and energy balance
8. document limitations and next refinement steps

The selected forced-air heatsink concept meets the 85 °C chip temperature target in the first-pass CFD model under the assumed 5 m/s guided airflow condition.