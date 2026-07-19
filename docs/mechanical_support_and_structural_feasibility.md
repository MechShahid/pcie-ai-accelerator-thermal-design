\# Mechanical Support and Structural Feasibility Screening



\## Purpose



This document adds a concept-level mechanical support check to the PCIe AI accelerator cooling project.



The final thermal candidate from the CFD design iteration is an 80 × 120 × 35 mm ducted aluminium heatsink. CFD-3 showed that this heatsink can meet the simplified 250 W chip cooling target, with a maximum chip temperature of 83.52 °C against an 85 °C target.



The purpose of this mechanical screening is to check whether the final heatsink concept is mechanically reasonable on a PCIe-style card, or whether additional support would likely be required.



This is a concept-level mechanical feasibility check only. It is not a detailed PCB structural analysis, PCIe compliance check, shock/vibration qualification, or validated mechanical design.



\## Final Thermal Candidate



| Quantity | Value |

|---|---:|

| Heatsink geometry | 80 × 120 × 35 mm |

| Base thickness | 5 mm |

| Fin height | 35 mm |

| Fin thickness | 1 mm |

| Number of fins | 26 |

| Material | Aluminium |

| Chip heat load | 250 W |

| CFD-3 maximum chip temperature | 83.52 °C |

| CFD-3 pressure drop | 49.02 Pa |

| Thermal result | Pass |



\## Mechanical Screening Method



The heatsink was approximated as a simple aluminium base plus straight rectangular fins.



The screening calculation estimated:



1\. base volume

2\. fin volume

3\. total aluminium volume

4\. heatsink mass

5\. weight force

6\. approximate bending moment

7\. support-risk category



The calculation used:



| Parameter | Value |

|---|---:|

| Aluminium density | 2700 kg/m³ |

| Gravity | 9.81 m/s² |

| Approximate lever arm | 35 mm |



The lever arm is a simplified screening assumption representing the approximate distance between the heatsink weight action and the PCB or support load path. It is not a detailed structural model.



\## Support-Risk Classification



A simple mass-based support-risk classification was used:



| Estimated heatsink mass | Support-risk level |

|---:|---|

| Less than 250 g | Low |

| 250–350 g | Medium |

| Greater than 350 g | High |



This classification is intended only for early engineering judgement. It does not replace mechanical design rules, PCIe specification checks, PCB stiffness analysis, or qualification testing.



\## Mechanical Screening Results



| Case | Geometry | Estimated mass | Weight force | Approx. bending moment | Support risk |

|---|---|---:|---:|---:|---|

| CFD-0 | 80 × 100 × 50 mm | 459.00 g | 4.50 N | 0.158 N·m | High |

| CFD-1 | 80 × 100 × 35 mm | 353.70 g | 3.47 N | 0.121 N·m | High |

| CFD-2 | 80 × 100 × 35 mm | 353.70 g | 3.47 N | 0.121 N·m | High |

| CFD-3 | 80 × 120 × 35 mm | 424.44 g | 4.16 N | 0.146 N·m | High |



The final CFD-3 candidate has an estimated heatsink mass of approximately 424.44 g. This is above the selected high-support-risk threshold of 350 g.



Therefore, although CFD-3 passed the thermal target, it should not be treated as mechanically complete without additional support.



\## Interpretation



The CFD-3 design is thermally feasible but mechanically support-sensitive.



The 80 × 120 × 35 mm aluminium heatsink provides enough heat-transfer area to meet the first-pass thermal target, but its estimated mass is relatively high for a PCIe-style add-in card. The calculated weight force is approximately 4.16 N, and the approximate bending moment is 0.146 N·m using the simplified 35 mm lever-arm assumption.



This suggests that the final heatsink should not rely only on the PCB for mechanical support.



\## Recommended Mechanical Support Concept



A practical mechanical design direction would include one or more of the following:



\- backplate behind the PCB

\- screw-mounted heatsink with load spreading

\- local stiffeners or standoffs near the chip region

\- bracket support connected to the card frame

\- chassis-supported duct or shroud

\- support points that reduce PCB bending and heatsink moment load



The duct used for thermal improvement could also contribute mechanically if it is designed as a chassis-supported airflow guide rather than only as a fluid-domain boundary.



\## Engineering Conclusion



The final CFD-3 heatsink concept meets the simplified thermal target but requires mechanical support consideration.



The project conclusion should therefore be stated as:



The ducted 80 × 120 × 35 mm aluminium heatsink is a passing first-pass thermal feasibility candidate for the simplified 250 W PCIe-style accelerator cooling problem. However, concept-level mechanical screening estimates a heatsink mass of approximately 424 g and classifies the design as high support risk. A backplate, bracket, standoffs, or chassis-supported duct is recommended before treating the design as mechanically feasible.



\## Limitations



This screening does not include:



\- detailed PCB stack-up

\- PCB bending stiffness

\- mounting-hole stresses

\- screw preload

\- contact pressure distribution

\- shock and vibration loads

\- PCIe mechanical compliance

\- fan or duct attachment loads

\- chassis interaction

\- detailed structural FEA

\- experimental mechanical validation



Further work would require detailed CAD assembly, mounting definition, PCB material stack-up, static structural FEA, and shock/vibration assessment.

