\# CFD 0: Chip + TIM + Heatsink + Guided Airflow



\## Purpose



This folder contains the first simplified CFD model for the PCIe AI accelerator thermal design study.



The model includes:



\- 45 × 45 × 2 mm chip

\- 0.2 mm TIM layer

\- 80 × 100 × 5 mm aluminum heatsink base

\- 26 straight plate fins

\- 1 mm fin thickness

\- 2 mm fin gap

\- 50 mm fin height

\- guided airflow at 5 m/s

\- 250 W chip heat load



\## Target



The CFD result will be compared against the analytical prediction:



T\_chip ≈ 82.4 °C



\## CFD 0 Scope



Included:



\- chip heat generation

\- TIM conduction

\- aluminum heatsink conduction

\- forced convection through fin channels

\- conjugate heat transfer



Excluded:



\- full PCB

\- memory

\- VRM

\- vapor chamber

\- radiation

\- detailed chassis

\- fan curve



\## Main Outputs Needed



\- maximum chip temperature

\- average chip temperature

\- outlet air temperature

\- pressure drop

\- velocity field

\- temperature field

\- heat balance

