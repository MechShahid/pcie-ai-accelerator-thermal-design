# Passive / Fanless Heatsink Screening

## Purpose

This study checks whether a purely passive / fanless heatsink can remove the 250 W chip heat load from a PCIe AI accelerator card.

The purpose of this step is not to create a final product design. The goal is to test the physical feasibility of passive cooling before moving to forced-air or more advanced cooling architectures.

## Heat Load and Target

| Parameter | Value |
|---|---:|
| Chip heat load | 250 W |
| Reference maximum chip / heatsink temperature | 85 °C |
| Open ambient temperature | 25 °C |
| Warm cabinet surroundings | 40 °C and 50 °C |

A passive solution is considered feasible only if the heatsink can reject approximately 250 W while keeping the surface temperature near the 85 °C target.

## Heatsink Geometries Studied

Two heatsink geometries were evaluated.

| Geometry | Width | Length | Fin height | Fin gap | Fin thickness |
|---|---:|---:|---:|---:|---:|
| Compact baseline | 80 mm | 80 mm | 25 mm | 2 mm | 1 mm |
| Larger candidate | 80 mm | 100 mm | 50 mm | 2 mm | 1 mm |

The compact baseline represents the original PCIe heatsink envelope.

The larger candidate represents an improved but still simple passive heatsink geometry.

## Material and Surface Finish

The heatsink is modelled as aluminum.

| Property | Value |
|---|---:|
| Material | Aluminum heatsink |
| Thermal conductivity | 200 W/mK |
| Emissivity cases | 0.20, 0.50, 0.85 |

The main reported passive result uses:

```text
black-anodized aluminum, emissivity = 0.85
```

This gives the passive concept a strong but realistic radiation advantage.

## Surface Treatment in the Model

The heatsink bottom surface is in contact with the chip / TIM stack. Therefore, it is not exposed to air.

```text
bottom convection = 0
bottom radiation  = 0
```

Only surfaces exposed to the surrounding air volume are included in natural convection and radiation.

| Surface group | Included? | Model |
|---|---:|---|
| Fin-channel walls | Yes | Elenbaas convection + Shabany radiation |
| Base area between fins | Yes | Channel convection/radiation |
| Fin tips | Yes | Exposed convection + gray-body radiation |
| Outer side faces | Yes | Exposed convection + gray-body radiation |
| Bottom surface touching TIM/chip | No | Conductive contact only |

## Heat-Transfer Models

### 1. Channel Natural Convection

Natural convection inside the fin channels is estimated using an Elenbaas-type vertical plate-channel correlation.

The modified Rayleigh number is written as:

```text
Ra* = [g beta (Ts - Tsur) S^3 / (nu alpha)] [S / Lg]
```

where:

| Symbol | Meaning |
|---|---|
| `S` | fin spacing / gap |
| `Lg` | channel dimension aligned with gravity |
| `Ts` | heatsink surface temperature |
| `Tsur` | surrounding temperature |

Two orientation cases are checked:

| Orientation case | Gravity-aligned length |
|---|---:|
| Best vertical channel case | fin height `Hf` |
| Length-aligned channel case | channel length `L` |

### 2. Exposed-Surface Natural Convection

Exposed fin tips and outer surfaces are estimated using a Churchill-Chu-type natural convection correlation for exposed surfaces.

This is used only for external exposed areas, not for the fin-channel walls.

### 3. Channel Radiation

Fin-channel radiation is calculated using the exact Shabany-type plate-fin channel view-factor formulation.

For one channel:

```text
A_ch = (S + 2Hf) L
```

The Shabany channel-to-surroundings factor is calculated from:

```text
Fs = [F14 + 2F15 + 2Hbar(F24 + 2F25)] / [1 + 2Hbar]
```

where:

```text
Lbar = L / S
Hbar = Hf / S
```

The channel radiation heat transfer is then:

```text
Q_rad,ch =
sigma A_ch (Ts^4 - Tsur^4)
/
[(1 - epsilon)/epsilon + 1/Fs]
```

For all channels:

```text
Q_rad,ch,total = N_channels Q_rad,ch
```

The finite radome receiver term used in the AAU paper is not used here, because the PCIe heatsink case is first treated as an open channel radiating to large surroundings.

### 4. Exposed-Surface Radiation

For fin tips and outer exposed surfaces, simple gray-body radiation to large surroundings is used:

```text
Q_rad,exposed = epsilon sigma A_exposed (Ts^4 - Tsur^4)
```

## Surrounding Conditions

Two types of surrounding conditions are evaluated.

| Case | Surrounding temperature | Meaning |
|---|---:|---|
| Open ambient | 25 °C | optimistic open-air passive limit |
| Warm cabinet | 40–50 °C | warmer enclosed chassis environment |

For the first screening, the same Shabany open-channel radiation model is used. The warm cabinet penalty is represented by increasing the surrounding temperature.

## Results at 85 °C Surface Temperature

The most important results are for black-anodized aluminum, emissivity = 0.85.

| Geometry | Orientation | Surrounding | Total passive heat rejection |
|---|---|---:|---:|
| Compact 80×80×25 mm | fin-height aligned | 25 °C | 25.1 W |
| Compact 80×80×25 mm | fin-height aligned | 40 °C | 16.9 W |
| Compact 80×80×25 mm | fin-height aligned | 50 °C | 12.0 W |
| Compact 80×80×25 mm | length aligned | 25 °C | 17.0 W |
| Larger 80×100×50 mm | fin-height aligned | 25 °C | 37.9 W |
| Larger 80×100×50 mm | fin-height aligned | 40 °C | 26.1 W |
| Larger 80×100×50 mm | fin-height aligned | 50 °C | 19.0 W |
| Larger 80×100×50 mm | length aligned | 25 °C | 30.6 W |

The best passive case is:

```text
Larger 80 × 100 × 50 mm heatsink
black-anodized aluminum
open ambient at 25 °C
surface temperature = 85 °C
Q_total ≈ 37.9 W
```

This is far below the required 250 W chip heat load.

## Contribution Breakdown

For the compact 80 × 80 × 25 mm heatsink at 85 °C surface temperature, open ambient, and emissivity 0.85:

| Contribution | Heat rejection |
|---|---:|
| Channel natural convection | 11.8 W |
| Channel radiation | 3.1 W |
| Exposed natural convection | 6.0 W |
| Exposed radiation | 4.2 W |
| Total | 25.1 W |

Radiation contributes:

```text
3.1 + 4.2 = 7.3 W
```

which is about:

```text
7.3 / 25.1 ≈ 29 %
```

So radiation is important, but it is not sufficient to make passive cooling feasible for a 250 W chip.

## Engineering Interpretation

The passive heatsink removes only a small fraction of the required chip heat load.

| Case | Best passive heat rejection | Required heat rejection |
|---|---:|---:|
| Compact heatsink | 25.1 W | 250 W |
| Larger candidate | 37.9 W | 250 W |

Even the larger passive candidate removes only:

```text
37.9 / 250 ≈ 15 %
```

of the required heat load.

Therefore, the passive architecture is not just slightly under-designed. It is fundamentally insufficient for this 250 W PCIe accelerator target.

## Conclusion

A purely fanless passive heatsink architecture is not feasible for the 250 W PCIe AI accelerator case considered here.

Even under optimistic conditions, using black-anodized aluminum, open ambient surroundings, natural convection, and exact Shabany channel radiation, the larger heatsink rejects only about 38 W at 85 °C.

The project should therefore proceed with active cooling architectures such as:

1. forced-air heatsink cooling,
2. vapor-chamber-assisted forced-air cooling,
3. or liquid cold plate cooling if airflow and mechanical constraints become too severe.

This result justifies excluding a purely passive fanless design from the main thermal architecture path.