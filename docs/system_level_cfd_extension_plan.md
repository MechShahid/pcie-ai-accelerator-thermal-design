# System-Level CFD Extension Plan

## Purpose

The first CFD model was a local chip–TIM–heatsink conjugate heat-transfer model with idealised guided airflow. It was useful as a Phase 1 thermal feasibility check, but it does not yet represent the full PCIe card or the enclosure/chamber airflow environment.

This document defines the next CFD extension needed to move from local heatsink feasibility toward board/system-level cooling assessment.

## Current CFD Status

The current CFD model includes:

| Item | Included |
|---|---|
| Chip heat source | Yes |
| TIM layer | Yes |
| Aluminium heatsink base and fins | Yes |
| Local air domain | Yes |
| Guided inlet velocity | Yes |
| Pressure outlet | Yes |
| Energy equation | Yes |
| Conjugate heat transfer | Yes |
| Full PCIe board | No |
| Memory and VRM heat loads | No |
| Enclosure or chamber | No |
| Fan curve | No |
| Bypass airflow | No |
| Mounting hardware | No |
| Mechanical keep-out constraints | No |

The Phase 1 result showed that the selected forced-air heatsink concept can keep the 250 W chip below the 85 °C target under the assumed 5 m/s guided-flow condition. However, this result should not yet be treated as final system performance.

## Why a System-Level CFD Extension Is Needed

In real hardware, the chip temperature is not controlled only by the heatsink geometry. It also depends on:

- Available system airflow
- Fan operating point
- Pressure drop through the full system
- Bypass flow around the heatsink
- Chassis or chamber restrictions
- Board-level heat sources
- Component blockage
- Inlet air temperature
- Recirculation near outlet regions
- Ducting and flow guidance
- Mechanical envelope constraints

The next CFD phase should therefore check whether the airflow assumed in Phase 1 can actually be delivered through the heatsink in a realistic system environment.

## Phase 2 CFD Objective

The objective of the system-level CFD model is to answer:

> Can the selected or mechanically constrained heatsink concept cool the 250 W chip when placed on a simplified PCIe card inside a realistic enclosure or airflow chamber?

The model should also evaluate whether a lower-height heatsink variant can meet the target when combined with better ducting or system airflow.

## Proposed Model Scope

The next CFD model should include:

| Feature | Purpose |
|---|---|
| Simplified PCIe board | Represent board-level integration |
| Chip, TIM, and heatsink | Main thermal path |
| Memory blocks | Include neighbouring heat sources |
| VRM block | Include power delivery heat load |
| Simplified enclosure/chamber | Represent system airflow restriction |
| Inlet region | Apply fan/mass-flow/velocity boundary condition |
| Outlet region | Reduce artificial recirculation |
| Bypass regions | Capture airflow not passing through heatsink |
| Duct option | Check improvement from guided airflow |
| Solid board material | Capture spreading through PCB approximately |

## Geometry Definition

### Board

Use a simplified PCIe-style board:

| Parameter | Suggested value |
|---|---:|
| Board length | 167.65 mm |
| Board height | 111.15 mm |
| Board thickness | 1.6 mm |

The board does not need full detailed electronics geometry at this stage. The goal is to include the main airflow obstruction and heat-source placement.

### Chip

| Parameter | Value |
|---|---:|
| Chip size | 45 mm × 45 mm |
| Chip thickness | 2 mm |
| Heat load | 250 W |

The chip should remain the dominant heat source.

### TIM

| Parameter | Value |
|---|---:|
| TIM thickness | 0.2 mm |
| Thermal conductivity | 6 W/mK |

TIM sensitivity can be tested later using 3, 6, and 8 W/mK.

### Heatsink Variants

The system-level CFD should not only test the current 50 mm tall heatsink. It should include mechanically constrained variants.

| Variant | Footprint | Fin height | Purpose |
|---|---:|---:|---|
| A | 80 × 100 mm | 50 mm | Current thermal candidate |
| B | 80 × 100 mm | 35 mm | Reduced-height option |
| C | 80 × 100 mm | 25 mm | More compact PCIe-style option |
| D | 80 × 120 mm | 35 mm | Longer, lower-profile option |
| E | 80 × 100 mm | 35 mm + duct | Reduced-height ducted option |

The 50 mm heatsink remains the Phase 1 reference, but the reduced-height cases are more important for mechanical feasibility.

### Memory Blocks

Add simplified memory packages around the chip.

| Parameter | Suggested value |
|---|---:|
| Number of memory blocks | 8 |
| Single block size | 14 × 12 × 1.5 mm |
| Total memory heat load | 40 W |

Memory heat can be applied as uniform volumetric heat generation inside each package.

### VRM Block

Add a simplified VRM region.

| Parameter | Suggested value |
|---|---:|
| VRM size | 60 × 15 × 3 mm |
| VRM heat load | 30 W |

The exact location can be approximate in the first system-level model, but it should be upstream or near the board edge depending on layout assumptions.

### Enclosure or Chamber

The enclosure should be simple and transparent in purpose. It does not need to represent a specific commercial server chassis.

Suggested first chamber:

| Parameter | Suggested value |
|---|---:|
| Chamber length | 250–300 mm |
| Chamber height | 70–90 mm |
| Chamber width | 120–150 mm |

The chamber should provide enough upstream and downstream distance to reduce artificial inlet/outlet effects.

## Boundary Conditions

### Thermal Boundary Conditions

| Item | Boundary condition |
|---|---|
| Chip | 250 W heat generation |
| Memory | 40 W total heat generation |
| VRM | 30 W total heat generation |
| Inlet air temperature | 25 °C baseline |
| Outer walls | Adiabatic for first model |
| Radiation | Off for first forced-air model |

Later sensitivity cases can include 35 °C and 45 °C inlet air.

### Flow Boundary Conditions

Start with three possible airflow approaches:

| Approach | Boundary condition | Purpose |
|---|---|---|
| Velocity inlet | 3, 5, 7 m/s | Compare with Phase 1 |
| Mass-flow inlet | Equivalent flow rate | Better for controlled system airflow |
| Fan boundary | Fan curve if available | Most realistic later step |

The first extension can still use velocity inlet, but the report should clearly state that fan-curve matching is required for product-level prediction.

## CFD Cases to Run

### Case 1: Reference System Model

| Setting | Value |
|---|---|
| Heatsink | 80 × 100 × 50 mm |
| Airflow | 5 m/s inlet |
| Heat loads | Chip only, 250 W |
| Purpose | Compare local CFD versus system CFD |

### Case 2: Full Board Heat Load

| Setting | Value |
|---|---|
| Heatsink | 80 × 100 × 50 mm |
| Airflow | 5 m/s inlet |
| Heat loads | Chip 250 W, memory 40 W, VRM 30 W |
| Purpose | Check effect of neighbouring heat sources |

### Case 3: Reduced-Height Heatsink

| Setting | Value |
|---|---|
| Heatsink | 80 × 100 × 35 mm |
| Airflow | 5 m/s inlet |
| Heat loads | Chip 250 W, memory 40 W, VRM 30 W |
| Purpose | Check mechanically safer variant |

### Case 4: Reduced-Height with Duct

| Setting | Value |
|---|---|
| Heatsink | 80 × 100 × 35 mm |
| Airflow | 5 m/s inlet |
| Duct | Yes |
| Heat loads | Chip 250 W, memory 40 W, VRM 30 W |
| Purpose | Check whether ducting compensates for reduced fin height |

### Case 5: Airflow Sensitivity

| Setting | Values |
|---|---|
| Heatsink | Best mechanically feasible variant |
| Airflow | 3, 5, 7 m/s |
| Heat loads | Full board |
| Purpose | Determine minimum airflow required |

### Case 6: Ambient Sensitivity

| Setting | Values |
|---|---|
| Inlet temperature | 25, 35, 45 °C |
| Heatsink | Best mechanically feasible variant |
| Heat loads | Full board |
| Purpose | Check thermal margin under warmer inlet conditions |

## Quantities to Extract

For each CFD case, extract:

| Quantity | Purpose |
|---|---|
| Maximum chip temperature | Main acceptance metric |
| Average chip temperature | Check heat-source distribution |
| Maximum memory temperature | Board-level risk |
| Maximum VRM temperature | Power-delivery risk |
| Inlet mass flow rate | Confirm actual flow |
| Outlet mass flow rate | Mass balance |
| Outlet air temperature | Heat balance |
| Pressure drop | Fan/system compatibility |
| Heat removed by air | Energy balance |
| Fraction of flow through heatsink | Bypass assessment |
| Velocity contours | Flow path interpretation |
| Temperature contours | Hotspot interpretation |
| Pressure contours | System impedance interpretation |

## Acceptance Criteria

The first engineering acceptance criteria should be:

| Criterion | Target |
|---|---:|
| Maximum chip temperature | < 85 °C |
| Heat balance error | < 5% for first-pass model, preferably < 2% |
| Mass imbalance | < 1% |
| Pressure drop | Reported and compared between variants |
| No severe outlet recirculation | Outlet extension adjusted if needed |
| Stable engineering monitors | Temperature and pressure stable with iterations |

For a portfolio-level first extension, the main goal is not perfect final convergence but a defensible engineering comparison between variants.

## Mesh Strategy

The mesh should be refined near:

- Chip
- TIM layer
- Heatsink base
- Fin channels
- Leading and trailing edges of heatsink
- Memory and VRM blocks
- Duct openings if included

Important checks:

- Minimum orthogonal quality
- Maximum skewness
- Boundary-layer resolution if turbulence is used
- Mesh independence for at least one representative case

A coarse model can be used first for trend comparison. A refined mesh should then be used for the selected final variant.

## Turbulence Model Consideration

The first Phase 1 model used laminar flow because the estimated channel Reynolds number was in the low-to-transitional range.

For the system-level chamber model, the flow may include:

- Jet-like inlet regions
- Separation
- Bypass flow
- Recirculation
- Obstructions from components
- Transitional or turbulent mixing

Therefore, the extension should compare:

| Model | Purpose |
|---|---|
| Laminar | Continuity with Phase 1 |
| k-omega SST | More realistic separated internal flow |
| Realizable k-epsilon | Alternative engineering turbulence model |

The final choice should be based on Reynolds number, stability, and comparison of predicted chip temperature and pressure drop.

## Ducting Study

A ducting study is important because the Phase 1 model assumes guided flow through the heatsink.

Compare:

| Design | Description |
|---|---|
| Open heatsink | Air can bypass around fins |
| Side-blocked heatsink | Less bypass flow |
| Simple inlet duct | More flow directed into fins |
| Full shroud | Maximum guided flow, higher pressure drop |

This will show whether the 5 m/s effective channel flow is realistic or only achievable with ducting.

## Fan and Pressure-Drop Interpretation

The Phase 1 pressure drop was approximately 28.8 Pa for the local domain. In a system-level model, pressure drop may increase due to:

- Inlet contraction
- Outlet expansion
- Ducting
- Board obstruction
- Component blockage
- Longer flow path
- Recirculation
- Filter or chassis restrictions

A later fan-curve analysis should check whether the fan can deliver the required flow at the predicted system pressure drop.

## Relationship to Mechanical Design

The system-level CFD should be run only after defining the mechanically feasible heatsink candidates.

Mechanical constraints may force:

- Lower fin height
- Longer heatsink
- Different fin spacing
- Copper or vapor-chamber base
- Heat pipes to remote fin stack
- Chassis-supported heatsink
- Ducted airflow

Therefore, the system-level CFD is not only a thermal extension. It is the link between mechanical design constraints and cooling performance.

## Expected Outcomes

The extension should produce one of the following conclusions:

| Outcome | Meaning |
|---|---|
| 50 mm heatsink passes but reduced-height fails | Thermal concept works, but mechanical constraints may require architecture change |
| 35 mm ducted heatsink passes | More realistic mechanically constrained solution |
| 25–35 mm heatsink fails | Need vapor chamber, heat pipes, cold plate, or stronger system airflow |
| Full-board heat load causes excessive temperature | Need memory/VRM cooling strategy |
| Bypass flow is severe | Need ducting or shroud |
| Pressure drop too high | Need lower restriction heatsink or stronger fan |

## Recommended Reporting Format

For each system CFD case, report:

```text
Case name:
Geometry:
Heat loads:
Airflow condition:
Max chip temperature:
Max memory temperature:
Max VRM temperature:
Outlet temperature:
Mass flow:
Pressure drop:
Heat balance error:
Main contour figures:
Engineering conclusion: