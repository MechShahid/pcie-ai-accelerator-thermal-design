# CFD Design Iteration Summary

## Purpose

This document summarizes the CFD design progression used to evaluate and improve the cooling concept for the simplified 250 W PCIe-style AI accelerator card.

The CFD work was not treated as a single black-box simulation. Instead, the workflow used step-by-step design iteration:

1. Test the reduced-height heatsink in an open/bypass domain.
2. Add ducting to reduce bypass.
3. Increase heatsink length to recover the remaining thermal margin.

The goal was to identify a lower-height aluminium heatsink concept capable of keeping the chip below the 85°C maximum temperature target under a 250 W heat load.

## Design Target

| Quantity | Value |
|---|---:|
| Chip power | 250 W |
| Inlet air temperature | 298.15 K = 25°C |
| Maximum chip-temperature target | 85°C |
| Cooling method | Forced-air heatsink |
| Material | Aluminium |
| Baseline lower-height fin height | 35 mm |

## CFD Case Overview

| Case | Geometry | Domain type | Main purpose |
|---|---|---|---|
| CFD-1 | 80 × 100 × 35 mm | Open/bypass | Test reduced-height heatsink in less constrained airflow |
| CFD-2 | 80 × 100 × 35 mm | Ducted | Reduce bypass and force more air through the fin region |
| CFD-3 | 80 × 120 × 35 mm | Ducted | Recover remaining thermal margin by increasing heatsink length |

## Numerical Comparison

| Quantity | CFD-1 | CFD-2 | CFD-3 |
|---|---:|---:|---:|
| Heatsink geometry | 80 × 100 × 35 mm | 80 × 100 × 35 mm | 80 × 120 × 35 mm |
| Domain type | Open/bypass | Ducted | Ducted |
| Maximum chip temperature | 91.47°C | 87.78°C | 83.52°C |
| Average chip temperature | 86.81°C | 83.12°C | 78.77°C |
| Outlet temperature | 29.91°C | 35.93°C | 35.96°C |
| Inlet mass flow rate | 0.05053125 kg/s | 0.02260125 kg/s | 0.02260125 kg/s |
| Pressure drop | 12.7 Pa | 44.54 Pa | 49.02 Pa |
| Heat-balance error | approximately 0.1% | approximately 0.6% | approximately 0.36% |
| Result | Fail | Slight fail | Pass |

## Temperature Target Comparison

| Case | Maximum chip temperature | Margin relative to 85°C target | Result |
|---|---:|---:|---|
| CFD-1 | 91.47°C | -6.47°C | Fail |
| CFD-2 | 87.78°C | -2.78°C | Slight fail |
| CFD-3 | 83.52°C | +1.48°C | Pass |

CFD-3 was the first lower-height aluminium heatsink case that passed the 85°C maximum chip-temperature target.

## Design Evolution

### CFD-1: Open/bypass 35 mm heatsink

CFD-1 tested the 80 × 100 × 35 mm aluminium heatsink in an open air-domain configuration.

The result showed:

- Maximum chip temperature: 91.47°C
- Pressure drop: 12.7 Pa
- Result: Fail

Although the inlet mass flow rate was high, the pressure drop was low and the flow-capture estimate was only about 34%. This indicated that a significant portion of the air bypassed the fin region instead of passing through the heatsink channels.

The main lesson from CFD-1 was that total inlet flow rate alone is not enough. Airflow delivery and bypass control are critical.

### CFD-2: Ducted 35 mm heatsink

CFD-2 kept the same 80 × 100 × 35 mm aluminium heatsink but used a ducted/shrouded air domain.

The result showed:

- Maximum chip temperature: 87.78°C
- Pressure drop: 44.54 Pa
- Result: Slight fail

Ducting increased the pressure drop from 12.7 Pa to 44.54 Pa, showing that more air was forced through the heatsink region. This reduced the maximum chip temperature from 91.47°C to 87.78°C.

However, the maximum chip temperature remained approximately 2.8°C above the 85°C target. CFD-2 therefore showed that ducting was beneficial, but the 100 mm long reduced-height heatsink still lacked sufficient heat-transfer area.

### CFD-3: Extended-length ducted 35 mm heatsink

CFD-3 increased the heatsink length from 100 mm to 120 mm while keeping the 35 mm fin height and ducted domain.

The result showed:

- Maximum chip temperature: 83.52°C
- Pressure drop: 49.02 Pa
- Result: Pass

Increasing the heatsink length from 100 mm to 120 mm reduced the maximum chip temperature by approximately 4.26°C compared with CFD-2.

The pressure drop increased only moderately:

49.02 Pa - 44.54 Pa = 4.48 Pa

This showed that increasing heatsink length was an effective way to recover the missing thermal margin while avoiding the mechanically more aggressive 50 mm fin-height design.

## Pressure-Drop Interpretation

The pressure-drop trend was physically consistent:

| Transition | Pressure-drop change | Interpretation |
|---|---:|---|
| CFD-1 to CFD-2 | 12.7 Pa to 44.54 Pa | Ducting reduced bypass and forced more flow through the heatsink region |
| CFD-2 to CFD-3 | 44.54 Pa to 49.02 Pa | Longer fins increased flow resistance moderately |

The CFD-2 pressure drop was also checked using a simple strict fin-gap analytical estimate. The hand estimate gave approximately 61 Pa, while CFD gave approximately 44.5 Pa. The difference was reasonable because the CFD model included three-dimensional redistribution and small side/top clearances, which increased the effective flow area compared with the strict idealized fin-gap model.

## Heat-Balance Check

The heat-balance checks were good for the CFD design iterations.

| Case | Approximate heat-balance error |
|---|---:|
| CFD-1 | approximately 0.1% |
| CFD-2 | approximately 0.6% |
| CFD-3 | approximately 0.36% |

For CFD-3:

- Inlet mass flow rate: 0.02260125 kg/s
- Air temperature rise: 10.96 K
- Estimated heat removed by air: approximately 249.1 W
- Applied chip heat load: 250 W

This gives a heat-balance error of approximately 0.36%, which supports the reliability of the engineering quantities extracted from the simulation.

## Final CFD Outcome

The best lower-height aluminium heatsink case from the CFD sequence was:

| Quantity | Final selected CFD case |
|---|---:|
| Case | CFD-3 |
| Heatsink geometry | 80 × 120 × 35 mm |
| Material | Aluminium |
| Domain | Ducted |
| Inlet velocity | 5 m/s |
| Chip heat load | 250 W |
| Maximum chip temperature | 83.52°C |
| Average chip temperature | 78.77°C |
| Pressure drop | 49.02 Pa |
| Heat-balance error | approximately 0.36% |
| Result | Pass |

## Engineering Conclusion

The CFD iteration showed that the reduced-height 35 mm heatsink could not pass the thermal target in an open/bypass configuration. Adding ducting significantly improved the result by reducing bypass, but the 100 mm long heatsink still remained slightly above the 85°C target.

Extending the ducted heatsink length from 100 mm to 120 mm recovered the missing thermal margin and reduced the maximum chip temperature to 83.52°C. This produced a passing first-pass CFD result with approximately 1.48°C margin below the 85°C target.

The final design direction is therefore:

- Use a ducted airflow path to control bypass.
- Keep the mechanically preferable 35 mm fin height.
- Increase heatsink length to 120 mm to recover thermal margin.
- Treat the 80 × 120 × 35 mm heatsink as the current thermal feasibility candidate.

## Limitations

This CFD result is a first-pass thermal feasibility result, not final product validation.

Further work would require:

- Mesh-sensitivity study
- Turbulence or transition model assessment
- Fan curve and system-level airflow modelling
- More realistic PCB, memory, and VRM heat sources
- Contact resistance and TIM sensitivity
- Mechanical support and mass evaluation
- PCB layout and component keep-out checks
- Experimental correlation with measured temperature and pressure drop

## Final Statement

The CFD design iteration successfully demonstrated a physics-based design workflow: identify a thermal failure, diagnose the airflow limitation, improve the ducting, and then modify the heatsink geometry to recover the required thermal margin.

The final CFD-3 case provides a defensible portfolio-level thermal feasibility result for a simplified 250 W PCIe-style AI accelerator cooling concept.