# CFD Design Iteration Summary

## Purpose

This document summarizes the CFD design progression used to evaluate and improve the cooling concept for the simplified 250 W PCIe-style AI accelerator card.

The CFD work was not treated as a single black-box simulation. Instead, the workflow used step-by-step design iteration:

1. Test the reduced-height heatsink in an open/bypass domain.
2. Add ducting to reduce bypass.
3. Increase heatsink length to recover the remaining thermal margin.
4. Repeat the final ducted case with a refined mesh.
5. Check viscous-model sensitivity using k-omega SST.

The goal was to identify a lower-height aluminium heatsink concept capable of keeping the chip below the 85°C maximum temperature target under a 250 W heat load, while also checking whether the conclusion remained reasonable under mesh refinement and turbulence-model sensitivity.

---

## Design Target

| Quantity | Value |
|---|---:|
| Chip power | 250 W |
| Inlet air temperature | 298.15 K = 25°C |
| Maximum chip-temperature target | 85°C |
| Cooling method | Forced-air heatsink |
| Material | Aluminium |
| Baseline lower-height fin height | 35 mm |

---

## CFD Case Overview

| Case | Geometry | Domain / model | Main purpose |
|---|---|---|---|
| CFD-1 | 80 × 100 × 35 mm | Open/bypass, laminar | Test reduced-height heatsink in less constrained airflow |
| CFD-2 | 80 × 100 × 35 mm | Ducted, laminar | Reduce bypass and force more air through the fin region |
| CFD-3 | 80 × 120 × 35 mm | Ducted, laminar | Recover remaining thermal margin by increasing heatsink length |
| CFD-4A | 80 × 120 × 35 mm | Ducted, refined mesh, laminar | Check mesh sensitivity of final ducted design |
| CFD-4B | 80 × 120 × 35 mm | Ducted, refined mesh, k-omega SST | Check viscous-model/turbulence sensitivity |

---

## Numerical Comparison

| Quantity | CFD-1 | CFD-2 | CFD-3 | CFD-4A | CFD-4B |
|---|---:|---:|---:|---:|---:|
| Heatsink geometry | 80 × 100 × 35 mm | 80 × 100 × 35 mm | 80 × 120 × 35 mm | 80 × 120 × 35 mm | 80 × 120 × 35 mm |
| Domain / model | Open/bypass, laminar | Ducted, laminar | Ducted, laminar | Ducted, refined mesh, laminar | Ducted, refined mesh, k-omega SST |
| Maximum chip temperature | 91.47°C | 87.78°C | 83.52°C | 78.11°C | 68.50°C |
| Average chip temperature | 86.81°C | 83.12°C | 78.77°C | 73.14°C | 63.58°C |
| Outlet temperature | 29.91°C | 35.93°C | 35.96°C | 35.98°C | 35.99°C |
| Inlet mass flow rate | 0.05053125 kg/s | 0.02260125 kg/s | 0.02260125 kg/s | 0.02260125 kg/s | 0.02260125 kg/s |
| Pressure drop | 12.7 Pa | 44.54 Pa | 49.02 Pa | 56.36 Pa | 83.84 Pa |
| Heat-balance error | approximately 0.1% | approximately 0.6% | approximately 0.36% | approximately 0.2% | approximately 0.1% |
| Result | Fail | Slight fail | Pass | Pass, mesh-sensitivity check | Pass, turbulence-model sensitivity check |

---

## Temperature Target Comparison

| Case | Maximum chip temperature | Margin relative to 85°C target | Result |
|---|---:|---:|---|
| CFD-1 | 91.47°C | -6.47°C | Fail |
| CFD-2 | 87.78°C | -2.78°C | Slight fail |
| CFD-3 | 83.52°C | +1.48°C | Pass |
| CFD-4A | 78.11°C | +6.89°C | Pass, mesh-sensitivity check |
| CFD-4B | 68.50°C | +16.50°C | Pass, turbulence-model sensitivity check |

CFD-3 was the first lower-height aluminium heatsink case that passed the 85°C maximum chip-temperature target.

CFD-4A and CFD-4B were added after CFD-3 to check sensitivity to mesh refinement and viscous-model choice. They should not be treated as final validation.

---

## Design Evolution

### CFD-1: Open/bypass 35 mm heatsink

CFD-1 tested the 80 × 100 × 35 mm aluminium heatsink in an open air-domain configuration.

The result showed:

- Maximum chip temperature: 91.47°C
- Pressure drop: 12.7 Pa
- Result: Fail

Although the inlet mass flow rate was high, the pressure drop was low and the flow-capture estimate was only about 34%. This indicated that a significant portion of the air bypassed the fin region instead of passing through the heatsink channels.

The main lesson from CFD-1 was that total inlet flow rate alone is not enough. Airflow delivery and bypass control are critical.

---

### CFD-2: Ducted 35 mm heatsink

CFD-2 kept the same 80 × 100 × 35 mm aluminium heatsink but used a ducted/shrouded air domain.

The result showed:

- Maximum chip temperature: 87.78°C
- Pressure drop: 44.54 Pa
- Result: Slight fail

Ducting increased the pressure drop from 12.7 Pa to 44.54 Pa, showing that more air was forced through the heatsink region. This reduced the maximum chip temperature from 91.47°C to 87.78°C.

However, the maximum chip temperature remained approximately 2.8°C above the 85°C target. CFD-2 therefore showed that ducting was beneficial, but the 100 mm long reduced-height heatsink still lacked sufficient heat-transfer area.

---

### CFD-3: Extended-length ducted 35 mm heatsink

CFD-3 increased the heatsink length from 100 mm to 120 mm while keeping the 35 mm fin height and ducted domain.

The result showed:

- Maximum chip temperature: 83.52°C
- Pressure drop: 49.02 Pa
- Result: Pass

Increasing the heatsink length from 100 mm to 120 mm reduced the maximum chip temperature by approximately 4.26°C compared with CFD-2.

The pressure drop increased only moderately:

```text
49.02 Pa - 44.54 Pa = 4.48 Pa
```

This showed that increasing heatsink length was an effective way to recover the missing thermal margin while avoiding the mechanically more aggressive 50 mm fin-height design.

---

### CFD-4A: Refined-mesh repeat of final ducted design

CFD-4A repeated the final CFD-3 ducted 80 × 120 × 35 mm heatsink case using a refined mesh.

The mesh was refined from approximately 188k elements in CFD-3 to approximately 511k elements in CFD-4A.

The result showed:

- Maximum chip temperature: 78.11°C
- Pressure drop: 56.36 Pa
- Result: Pass, mesh-sensitivity check

Compared with CFD-3:

```text
Maximum chip temperature changed by approximately -5.41°C
Pressure drop increased by approximately +7.34 Pa
```

The refined mesh still predicted that the design passed the 85°C target. However, the temperature change was significant enough that CFD-4A should be described as a mesh-sensitivity check, not as proof of mesh-independent CFD validation.

---

### CFD-4B: k-omega SST sensitivity case

CFD-4B repeated the refined CFD-4A case using the k-omega SST turbulence model.

The geometry, mesh, heat load, material properties, and boundary conditions were kept the same as CFD-4A. Only the viscous model was changed from laminar to k-omega SST.

The result showed:

- Maximum chip temperature: 68.50°C
- Pressure drop: 83.84 Pa
- Result: Pass, turbulence-model sensitivity check

Compared with CFD-4A:

```text
Maximum chip temperature changed by approximately -9.61°C
Pressure drop increased by approximately +27.48 Pa
```

The SST case predicted stronger cooling and higher pressure drop than the refined laminar case. This is physically understandable because the turbulence model adds stronger momentum and thermal mixing.

However, the result does not mean that the real flow is definitely fully turbulent. The estimated fin-channel Reynolds number was near the transitional range, so CFD-4B should be treated only as a viscous-model sensitivity check.

---

## Pressure-Drop Interpretation

The pressure-drop trend was physically consistent:

| Transition | Pressure-drop change | Interpretation |
|---|---:|---|
| CFD-1 to CFD-2 | 12.7 Pa to 44.54 Pa | Ducting reduced bypass and forced more flow through the heatsink region |
| CFD-2 to CFD-3 | 44.54 Pa to 49.02 Pa | Longer fins increased flow resistance moderately |
| CFD-3 to CFD-4A | 49.02 Pa to 56.36 Pa | Refined mesh resolved the ducted flow resistance differently |
| CFD-4A to CFD-4B | 56.36 Pa to 83.84 Pa | SST predicted stronger mixing and higher flow resistance |

The CFD-2 pressure drop was also checked using a simple strict fin-gap analytical estimate. The hand estimate gave approximately 61 Pa, while CFD gave approximately 44.5 Pa. The difference was reasonable because the CFD model included three-dimensional redistribution and small side/top clearances, which increased the effective flow area compared with the strict idealized fin-gap model.

---

## Heat-Balance Check

The heat-balance checks were good for the CFD design iterations.

| Case | Approximate heat-balance error |
|---|---:|
| CFD-1 | approximately 0.1% |
| CFD-2 | approximately 0.6% |
| CFD-3 | approximately 0.36% |
| CFD-4A | approximately 0.2% |
| CFD-4B | approximately 0.1% |

For CFD-3:

- Inlet mass flow rate: 0.02260125 kg/s
- Air temperature rise: 10.96 K
- Estimated heat removed by air: approximately 249.1 W
- Applied chip heat load: 250 W

This gives a heat-balance error of approximately 0.36%, which supports the reliability of the engineering quantities extracted from the simulation.

For CFD-4A and CFD-4B, the outlet temperature and heat balance remained consistent with the 250 W applied heat load, supporting their use as sensitivity comparisons.

---

## Mesh and Viscous-Model Sensitivity

CFD-4A showed that the final design remained thermally feasible after mesh refinement, but the maximum chip temperature changed by approximately 5.4°C compared with CFD-3. Therefore, the CFD-4A result supports thermal feasibility but does not prove mesh independence.

CFD-4B showed that the final design also remained below the 85°C target when the k-omega SST model was used. However, SST predicted a much lower chip temperature and higher pressure drop than the refined laminar case. Therefore, the detailed numerical prediction is sensitive to viscous-model choice.

The safe interpretation is:

```text
The final ducted heatsink remains thermally feasible under both refined laminar and k-omega SST assumptions, but further mesh refinement, near-wall checks, transition/turbulence modelling, and experimental correlation would be required before claiming validated CFD accuracy.
```

---

## Final CFD Outcome

The best lower-height aluminium heatsink design direction from the CFD sequence was:

| Quantity | Final selected design direction |
|---|---:|
| Heatsink geometry | 80 × 120 × 35 mm |
| Material | Aluminium |
| Domain | Ducted |
| Inlet velocity | 5 m/s |
| Chip heat load | 250 W |
| CFD-3 maximum chip temperature | 83.52°C |
| CFD-3 average chip temperature | 78.77°C |
| CFD-3 pressure drop | 49.02 Pa |
| CFD-4A refined-mesh maximum chip temperature | 78.11°C |
| CFD-4A pressure drop | 56.36 Pa |
| CFD-4B SST maximum chip temperature | 68.50°C |
| CFD-4B pressure drop | 83.84 Pa |
| Result | Thermally feasible in first-pass CFD and sensitivity checks |

CFD-3 is the main first-pass passing design case. CFD-4A and CFD-4B support the thermal feasibility conclusion but should be treated as sensitivity checks rather than final validation.

---

## Engineering Conclusion

The CFD iteration showed that the reduced-height 35 mm heatsink could not pass the thermal target in an open/bypass configuration. Adding ducting significantly improved the result by reducing bypass, but the 100 mm long heatsink still remained slightly above the 85°C target.

Extending the ducted heatsink length from 100 mm to 120 mm recovered the missing thermal margin and reduced the maximum chip temperature to 83.52°C. This produced a passing first-pass CFD result with approximately 1.48°C margin below the 85°C target.

A refined-mesh repeat then confirmed that the design remained below the target, but the 5.4°C change in chip temperature showed that the result was not fully mesh independent.

A k-omega SST sensitivity case predicted stronger cooling and higher pressure drop, confirming that the design remained thermally feasible under another viscous-model assumption. However, the large difference between the laminar and SST results showed that transition/turbulence modelling and experimental correlation would be needed before claiming final CFD accuracy.

The final design direction is therefore:

- Use a ducted airflow path to control bypass.
- Keep the mechanically preferable 35 mm fin height.
- Increase heatsink length to 120 mm to recover thermal margin.
- Treat the 80 × 120 × 35 mm heatsink as the current thermal feasibility candidate.
- Treat CFD-4A and CFD-4B as sensitivity checks, not final validation.

---

## Limitations

This CFD result is a first-pass thermal feasibility result, not final product validation.

Further work would require:

- additional mesh refinement and local near-wall/interface checks
- transition or turbulence model assessment
- fan curve and system-level airflow modelling
- more realistic PCB, memory, and VRM heat sources
- contact resistance and TIM sensitivity
- mechanical support and mass evaluation
- PCB layout and component keep-out checks
- PCB structural FEA
- shock and vibration assessment
- experimental correlation with measured temperature and pressure drop
- pressure-drop comparison with fan/system capability

---

## Final Statement

The CFD design iteration successfully demonstrated a physics-based design workflow: identify a thermal failure, diagnose the airflow limitation, improve the ducting, modify the heatsink geometry to recover the required thermal margin, then check sensitivity to mesh refinement and viscous-model choice.

The final CFD-3 case provides a defensible portfolio-level thermal feasibility result for a simplified 250 W PCIe-style AI accelerator cooling concept. CFD-4A and CFD-4B strengthen the workflow by showing that the design remains thermally feasible under refined-mesh and k-omega SST sensitivity checks, while also clearly identifying the need for further validation before claiming product-level CFD accuracy.
