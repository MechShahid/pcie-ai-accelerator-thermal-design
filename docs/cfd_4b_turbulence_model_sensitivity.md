# CFD-4B Turbulence-Model Sensitivity Results

## Purpose

CFD-4B was added as a turbulence-model sensitivity check for the final ducted heatsink design.

The earlier CFD cases used a laminar model as a first-pass assumption. Because the ducted fin-channel flow may be close to the transitional range, CFD-4B repeats the refined-mesh CFD-4A case using the k-omega SST turbulence model.

The purpose is not to prove that SST is the correct final model. The purpose is to check whether the thermal feasibility conclusion changes strongly when a turbulence model is used.

---

## Case description

| Quantity | Value |
|---|---:|
| Geometry | 80 × 120 × 35 mm ducted heatsink |
| Chip heat load | 250 W |
| Inlet air velocity | 5 m/s |
| Inlet air temperature | 25 °C |
| Mesh | CFD-4A refined mesh |
| Viscous model | k-omega SST |
| Turbulence intensity | 5% |
| Turbulent viscosity ratio | 10 |
| Iterations | 700 |

The geometry, mesh, materials, heat load, and boundary conditions were kept the same as CFD-4A. Only the viscous model was changed from laminar to k-omega SST.

---

## Mesh summary

The CFD-4B case used the same refined mesh as CFD-4A.

| Mesh quantity | Value |
|---|---:|
| Nodes | 191,534 |
| Elements | 511,566 |
| Maximum aspect ratio | 10.716 |
| Minimum element quality | 0.186 |
| Minimum orthogonal quality | 0.201 |

---

## Residual behaviour

At 700 iterations, the residuals were:

| Residual | Value |
|---|---:|
| Continuity | approximately 2.83e-2 |
| x-velocity | approximately 1.09e-5 |
| y-velocity | approximately 7.29e-6 |
| z-velocity | approximately 1.22e-5 |
| Energy | approximately 5.25e-6 |
| k | approximately 3.26e-4 |
| omega | approximately 2.12e-4 |

The SST case showed lower continuity residuals than the refined laminar CFD-4A case.

---

## CFD-4B SST results

| Quantity | CFD-4B result |
|---|---:|
| Maximum chip temperature | 341.65 K = 68.50 °C |
| Average chip temperature | 336.73 K = 63.58 °C |
| Outlet mass-weighted temperature | 309.14 K = 35.99 °C |
| Air temperature rise | 10.99 K |
| Inlet mass flow rate | 0.02260125 kg/s |
| Outlet mass flow rate | -0.022601869 kg/s |
| Mass imbalance | approximately 0.00274% |
| Inlet area-weighted static pressure | 83.843 Pa |
| Outlet area-weighted static pressure | 0 Pa |
| Pressure drop | 83.84 Pa |

---

## Heat balance

The air-side heat removal was estimated using:

```text
Q_air = m_dot cp ΔT
```

Using:

```text
m_dot = 0.02260125 kg/s
cp = 1006 J/kgK
ΔT = 309.13641 - 298.15 = 10.98641 K
```

gives:

```text
Q_air ≈ 249.7 W
```

For a 250 W chip heat load, this gives an energy balance error of approximately:

```text
Energy balance error ≈ 0.1%
```

This is a good heat-balance result for the turbulence-model sensitivity case.

---

## Comparison with laminar cases

| Case | Viscous model | Mesh | Maximum chip temperature | Pressure drop |
|---|---|---|---:|---:|
| CFD-3 | Laminar | Baseline mesh | 83.52 °C | 49.02 Pa |
| CFD-4A | Laminar | Refined mesh | 78.11 °C | 56.36 Pa |
| CFD-4B | k-omega SST | Refined mesh | 68.50 °C | 83.84 Pa |

---

## Interpretation

The k-omega SST case predicts a lower chip temperature than the refined laminar case.

Compared with CFD-4A:

```text
Temperature change = 78.11 - 68.50 = 9.61 °C lower
Pressure-drop change = 83.84 - 56.36 = 27.48 Pa higher
```

This indicates that the SST model is adding stronger momentum and thermal mixing, which increases heat transfer and also increases the predicted flow resistance.

The design remains below the 85 °C maximum chip-temperature target under both the refined laminar and k-omega SST assumptions.

However, the difference between CFD-4A and CFD-4B is significant. Therefore, the result should be treated as a turbulence-model sensitivity check, not as final validated CFD performance.

---

## Visualization note

For clarity, the CFD-4B temperature visualization is shown on the solid component surfaces rather than only on the centre cut plane. The centre cut plane intersects many thin fins, air gaps, and solid-fluid interfaces, which can produce a fragmented visual cut.

The numerical results and balance checks are therefore the main evidence for this sensitivity study.

---

## Conclusion

CFD-4B was completed as a k-omega SST sensitivity case using the same refined mesh, geometry, heat load, and boundary conditions as CFD-4A.

The SST case predicted a maximum chip temperature of 68.50 °C and a pressure drop of 83.84 Pa. Compared with the refined laminar case, SST predicted stronger cooling and higher pressure drop.

The final ducted heatsink design remains thermally feasible under both laminar and SST assumptions. However, the difference between the two cases shows that the final prediction is sensitive to viscous-model choice. Further transition/turbulence assessment, mesh refinement, near-wall checks, and experimental correlation would be required before treating the CFD result as validated product performance.

---

## Files generated

```text
cfd/cfd_4b_80x120x35_ducted_sst_sensitivity/results/cfd_4b_sst_700iter.cas.h5
cfd/cfd_4b_80x120x35_ducted_sst_sensitivity/results/cfd_4b_sst_700iter.dat.h5

cfd/cfd_4b_80x120x35_ducted_sst_sensitivity/screenshots/cfd_4b_temperature_solid_surfaces.png
cfd/cfd_4b_80x120x35_ducted_sst_sensitivity/screenshots/cfd_4b_static_pressure_center_x_plane.png
```