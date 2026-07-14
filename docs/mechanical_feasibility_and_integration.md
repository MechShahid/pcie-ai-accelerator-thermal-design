# Mechanical Feasibility and Integration Check

## Purpose

This document checks whether the thermally selected heatsink concept from the first-phase analytical and CFD study is mechanically realistic for a PCIe-style AI accelerator card.

The current thermal model demonstrated that a larger forced-air heatsink can remove the 250 W chip heat load under idealised guided-airflow conditions. However, the selected 80 mm × 100 mm × 50 mm heatsink should not be treated as a final product design until mechanical constraints, card integration, mounting, airflow access, and system-level enclosure effects are assessed.

## Current Status of the Thermal Concept

The current selected concept is:

| Parameter | Value |
|---|---:|
| Chip heat load | 250 W |
| Chip size | 45 mm × 45 mm |
| TIM thickness | 0.2 mm |
| TIM conductivity | 6 W/mK |
| Heatsink footprint | 80 mm × 100 mm |
| Fin height | 50 mm |
| Fin gap | 2 mm |
| Fin thickness | 1 mm |
| Assumed inlet airflow | 5 m/s guided airflow |
| First-pass CFD maximum chip temperature | approximately 76 °C |
| Target chip temperature | 85 °C |
| First-pass CFD pressure drop | approximately 28.8 Pa |

The result is thermally promising, but it is based on a simplified open/guided-airflow model. It does not yet include full PCIe chassis constraints, bypass airflow, fan curve, mounting details, PCB bending, or neighbouring component heat sources.

## Key Mechanical Feasibility Questions

Before the heatsink concept can be considered mechanically feasible, the following questions must be answered:

1. Does the 80 mm × 100 mm footprint fit within the available board area?
2. Is the 50 mm fin height acceptable for the intended chassis or system envelope?
3. Can the heatsink be mounted without excessive PCB bending?
4. Can the required TIM bondline thickness and contact pressure be controlled?
5. Is the airflow path realistic, or does the model require ducting?
6. Will bypass flow reduce the effective flow through the fin channels?
7. Are memory, VRM, connectors, capacitors, and mechanical keep-out zones respected?
8. Is the heatsink mass acceptable for handling, transport, vibration, and long-term reliability?
9. Can the concept be manufactured using standard extrusion, machining, skiving, or bonded-fin methods?
10. Is the concept suitable for supplier discussion, or does it require further simplification?

## PCIe Card Envelope Considerations

The current thermal concept should be checked against a realistic PCIe add-in card envelope.

Important integration constraints include:

- Card length and height
- Component keep-out regions
- Slot spacing
- Adjacent card clearance
- Chassis lid clearance
- Airflow direction
- Power connector location
- Bracket and mounting constraints
- Structural support for heavy heatsinks

The 50 mm fin height is mechanically aggressive for many PCIe systems. It may be acceptable in some server or development-platform configurations, but it may not be acceptable in compact workstations, edge devices, or dense multi-card systems.

Therefore, the 80 mm × 100 mm × 50 mm heatsink should be described as a thermal candidate, not a final mechanical design.

## Mechanical Risk Assessment

| Risk | Severity | Comment |
|---|---:|---|
| Fin height may exceed available chassis clearance | High | 50 mm is large for a PCIe card and must be checked against the target enclosure |
| Heatsink mass may bend PCB | Medium to High | A large aluminium heatsink may require backplate, stiffener, or bracket support |
| TIM bondline may vary under uneven mounting pressure | Medium | Thermal result assumes controlled 0.2 mm TIM thickness |
| Bypass airflow may reduce effective fin-channel flow | High | Open CFD does not yet model full chassis airflow distribution |
| Nearby components may disturb airflow | Medium | Memory, VRM, capacitors, and connectors were not included in the first CFD model |
| Pressure drop may change in enclosure | Medium | Current pressure drop is from simplified local domain only |
| Manufacturability of thin-fin design | Medium | 1 mm fins and 2 mm gaps may be feasible but require supplier/manufacturing check |
| Serviceability and assembly tolerance | Medium | Mounting method and repeatability are not yet defined |
| Vibration/shock reliability | Medium | Heavy heatsink requires mechanical retention assessment |

## Mounting and TIM Integration

The thermal model assumes a uniform TIM layer between the chip and heatsink base. In a real design, this depends on the mechanical mounting system.

Important mounting considerations:

- Screw pattern around the chip
- Spring screws or controlled-load fasteners
- Backplate or stiffener to reduce PCB bending
- TIM compression behaviour
- Bondline thickness control
- Flatness of chip lid and heatsink base
- Assembly repeatability
- Rework and serviceability

The current model assumes a 0.2 mm TIM thickness and 6 W/mK conductivity. This should be treated as a controlled design assumption. If the actual bondline becomes thicker, or if contact resistance is higher, the chip temperature will increase.

## PCB Bending and Structural Support

A large heatsink can create mechanical loading on the PCB due to:

- Heatsink self-weight
- Screw preload
- Handling loads
- Transport vibration
- Thermal cycling
- Chassis orientation

Possible mitigation options include:

- Metal backplate behind the PCB
- Mechanical bracket connected to the chassis
- Stiffener frame around the chip
- Spring-loaded screws
- Reduced heatsink height or mass
- Heat pipe or vapor chamber spreading to a remote fin stack

For a production-style design, the heatsink should not rely only on the PCB for support if the mass is high.

## Airflow Integration

The current CFD model assumes guided 5 m/s airflow entering the heatsink region. In a real system, the effective airflow through the fins depends on the system fan, ducting, enclosure, and bypass paths.

Important airflow questions:

- Is the airflow parallel to the fins?
- Is the heatsink ducted or open to the chassis?
- What fraction of the total system airflow passes through the fin channels?
- Does air bypass around the heatsink?
- Are there upstream blockages?
- Is the outlet far enough downstream to avoid recirculation?
- Does the pressure drop match the available fan operating point?

The next CFD phase should therefore include a simplified enclosure or chamber model.

## Manufacturability Considerations

The current concept uses:

- 1 mm fin thickness
- 2 mm fin spacing
- 50 mm fin height
- 100 mm fin length
- 80 mm heatsink width

Potential manufacturing routes include:

- Extruded aluminium heatsink
- Skived-fin heatsink
- Bonded-fin heatsink
- Machined prototype
- Vapor chamber base with fin stack
- Heat-pipe-assisted remote fin stack

For a first prototype, a machined or commercially similar heatsink may be acceptable. For production, supplier input is required to confirm fin geometry, tolerances, cost, mass, and manufacturability.

## Cooling Architecture Implications

The mechanical feasibility check may change the cooling architecture.

Possible outcomes:

| Outcome | Meaning |
|---|---|
| 80 × 100 × 50 mm heatsink fits | Continue with system-level CFD and validation plan |
| 50 mm height does not fit | Reduce fin height and compensate with higher airflow, ducting, copper base, vapor chamber, or heat pipes |
| PCB cannot support heatsink mass | Add backplate, chassis bracket, or remote cooling solution |
| Airflow is not sufficient | Add ducting, fan selection, lower pressure-drop geometry, or different cooling architecture |
| Local heatsink cannot meet target | Consider vapor chamber, heat pipes, cold plate, or system-level airflow redesign |

## Recommended Next Design Variants

To connect mechanical constraints back to thermal design, the following variants should be evaluated next:

| Variant | Purpose |
|---|---|
| 80 × 100 × 50 mm heatsink | Current thermal candidate |
| 80 × 100 × 35 mm heatsink | Reduced-height mechanically safer option |
| 80 × 100 × 25 mm heatsink | More compact PCIe-style option |
| 80 × 120 × 35 mm heatsink | Longer but lower profile option |
| Vapor chamber base + 35 mm fin stack | Improve spreading while reducing height |
| Heat-pipe-assisted remote fin stack | Move heat to a mechanically convenient airflow region |
| Ducted 35 mm heatsink | Improve effective flow through shorter fins |

These variants should be screened analytically first and then tested in a system-level CFD extension.

## Recommended System-Level CFD Extension

The next CFD model should include:

- PCIe-style board outline
- Chip, TIM, heatsink, memory, and VRM blocks
- Simplified enclosure or chamber
- Inlet and outlet vents
- Fan or mass-flow boundary condition
- Bypass flow around the heatsink
- Longer downstream outlet region
- Pressure drop through the heatsink and system path
- Chip, memory, and VRM temperatures

This would convert the current local heatsink CFD into a more realistic board/system-level cooling assessment.

## Engineering Interpretation

The first-phase thermal result shows that the 250 W heat load may be removable with an aggressive forced-air heatsink under guided airflow. However, the current geometry is mechanically aggressive and requires further integration checks.

The main mechanical concern is the 50 mm fin height. This may be acceptable for a server-style or development-platform environment, but it is not automatically compatible with every PCIe accelerator card enclosure.

Therefore, the correct conclusion is:

The current heatsink is a thermally promising candidate, but not yet a mechanically validated product design.

## Limitations of This Mechanical Check

This document is a feasibility-level review only. It does not yet include:

- Detailed CAD assembly
- Supplier manufacturing drawings
- PCIe compliance envelope verification
- Structural FEA
- PCB warpage analysis
- Vibration analysis
- Screw preload calculation
- Measured TIM compression data
- Fan curve and system impedance matching
- Physical prototype testing

## Recommended Next Steps

1. Define target mechanical envelope for the PCIe card.
2. Check whether 50 mm fin height is acceptable.
3. Estimate heatsink mass and PCB loading.
4. Define mounting concept with backplate or stiffener.
5. Create reduced-height heatsink variants.
6. Repeat analytical thermal screening for mechanically constrained variants.
7. Build simplified enclosure/chamber CFD model.
8. Add memory and VRM heat loads.
9. Create validation plan for heater-block testing.
10. Compare CFD predictions with planned test measurements.

## Summary

The current 80 mm × 100 mm × 50 mm heatsink concept should be kept as the Phase 1 thermal candidate. It is useful because it demonstrates that forced-air cooling can potentially meet the 250 W chip target under guided airflow.

However, the project should now move into Phase 2 mechanical integration. The next design decision is not only whether the heatsink cools the chip, but whether it can fit, mount, survive, and receive realistic airflow inside the intended system environment.