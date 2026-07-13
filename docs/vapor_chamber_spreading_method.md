\# Vapor-Chamber-Assisted Spreading Resistance Method



\## Purpose



This study adds the missing chip-to-base spreading resistance to the forced-air PCIe AI accelerator thermal model.



The previous forced-air model estimated the air-side heat rejection of the fin stack. It did not explicitly resolve the three-dimensional spreading resistance caused by transferring 250 W from a 45 mm × 45 mm chip into a larger heatsink base.



The purpose of this step is to determine whether reducing spreading resistance using a copper spreader or vapor chamber meaningfully reduces chip temperature, or whether the design remains dominated by air-side resistance.



\## Thermal Resistance Network



The chip-to-air resistance network is written as:



```text

R\_total = R\_TIM + R\_base,1D + R\_spreading + R\_air

```



where:



| Term | Meaning |

|---|---|

| `R\_TIM` | thermal interface material resistance |

| `R\_base,1D` | one-dimensional conduction through the base thickness |

| `R\_spreading` | excess spreading resistance from chip footprint to larger base |

| `R\_air` | forced-air fin-stack resistance from the existing heat-exchanger model |



The chip temperature is then:



```text

T\_chip = T\_air,in + Q\_chip × R\_total

```



\## TIM Model



The TIM is first modelled using bulk conduction:



```text

R\_TIM = t\_TIM / (k\_TIM A\_source)

```



Baseline values:



| Parameter | Value |

|---|---:|

| TIM thickness | 0.2 mm |

| TIM conductivity | 6 W/mK |

| Source area | 45 mm × 45 mm |

| R\_TIM | approximately 0.0165 K/W |



A sensitivity range of 3–8 W/mK is used for electronics-cooling TIMs. Interface contact resistances on both sides of the TIM are not resolved in the first-order model.



\## Spreading Resistance Model



The base spreading resistance is calculated using an electronics-cooling spreading-resistance method based on the Lee / Song / Au / Moran approach.



The rectangular source and base areas are converted into equivalent circular areas:



```text

a = sqrt(A\_source / pi)

b = sqrt(A\_base / pi)

```



where:



| Symbol | Meaning |

|---|---|

| `a` | equivalent source radius |

| `b` | equivalent base radius |

| `A\_source` | chip contact area |

| `A\_base` | heatsink base area |



The relevant non-dimensional parameters are:



```text

epsilon = a / b

tau = t\_base / b

Bi = h\_eff b / k

```



The spreading model accounts for the fact that the heat source area is smaller than the base area.



\## Air-Side Coupling



The air-side model already provides the fin-stack thermal resistance:



```text

R\_air

```



To provide the spreading model with a consistent convective boundary condition, an effective heat-transfer coefficient is calculated as:



```text

h\_eff = 1 / (R\_air A\_base)

```



The full base area is used, not the chip area.



This avoids double-counting the air-side resistance.



\## Base / Spreader Architectures



The same geometry and air-side resistance are compared for different spreading architectures:



| Case | Model |

|---|---|

| Aluminum base | isotropic solid conduction |

| Copper spreader | isotropic solid conduction |

| Vapor chamber conservative | equivalent anisotropic heat spreader |

| Vapor chamber optimistic | equivalent anisotropic heat spreader |



\## Aluminum and Copper



For solid metallic bases, the spreading resistance is calculated using isotropic conductivity:



| Material | Conductivity |

|---|---:|

| Aluminum | 167–200 W/mK |

| Copper | 385–400 W/mK |



\## Vapor Chamber Representation



The vapor chamber is not modelled as a detailed two-phase device.



Instead, it is represented as an equivalent anisotropic heat spreader:



```text

kx = ky >> kz

```



where:



| Direction | Meaning |

|---|---|

| `kx`, `ky` | high in-plane spreading conductivity |

| `kz` | lower through-thickness effective conductivity |



This captures the main useful role of the vapor chamber: improving lateral heat spreading from the chip to the heatsink base.



Internal vapor chamber limits such as capillary limit, boiling limit, sonic limit, entrainment limit and dry-out are not resolved because they require product-specific manufacturer data.



\## Comparison Objective



For each base architecture, calculate:



```text

R\_solid = R\_TIM + R\_base,1D + R\_spreading

```



and:



```text

R\_total = R\_solid + R\_air

```



Then compare:



```text

T\_chip = 25°C + 250 W × R\_total

```



The key engineering question is:



```text

Does reducing spreading resistance meaningfully reduce chip temperature, or is the design still dominated by air-side resistance?

```



\## Expected Interpretation



If reducing spreading resistance only lowers chip temperature by a few degrees, then the design is air-side limited.



If reducing spreading resistance lowers chip temperature significantly, then copper or vapor chamber spreading is important.



The vapor chamber is therefore evaluated as a hotspot and margin-improvement technology, not as a replacement for sufficient airflow and fin area.

