\# Airflow Sanity Check



\## Purpose



This document explains the airflow heat-capacity and flow-regime sanity check used before moving to CAD and CFD.



The goal is to check whether the assumed airflow velocities can physically carry away the heat load from the PCIe AI accelerator card.



This step was added before detailed CFD because a thermal resistance target alone does not prove that enough air is available to remove the heat.



\## Why This Check Is Needed



The chip-level thermal target is:



```text

R\_required = (T\_chip,max - T\_air,inlet) / Q\_chip

