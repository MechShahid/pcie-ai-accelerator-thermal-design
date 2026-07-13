"""
Passive / fanless heatsink screening model for a PCIe AI accelerator.

Purpose
-------
Estimate whether a plate-fin aluminum heatsink can reject 250 W passively
using:

1. Natural convection from fin channels
2. Natural convection from exposed surfaces
3. Channel radiation using exact Shabany-type view factor Fs
4. Exposed-surface gray-body radiation

Important modelling assumptions
-------------------------------
- The heatsink bottom surface is in contact with the chip/TIM stack.
  Therefore, the bottom surface is NOT included in convection or radiation.
- Fin-channel radiation uses exact Shabany-type plate-fin channel factor Fs.
- The AAU/radome finite receiver radiation formula is NOT used here.
  This PCIe model first assumes open channels radiating to large surroundings.
- A warm cabinet case is represented by higher surroundings temperature.
"""

import math
import csv
import os


# ============================================================
#  CONSTANTS
# ============================================================

SIGMA = 5.670374419e-8       # Stefan-Boltzmann constant [W/m2/K4]
G = 9.81                     # gravity [m/s2]

# Air properties, approximate near room temperature
K_AIR = 0.0263               # air thermal conductivity [W/m/K]
RHO_AIR = 1.184              # density [kg/m3]
CP_AIR = 1007.0              # specific heat [J/kg/K]
MU_AIR = 1.85e-5             # dynamic viscosity [Pa.s]

NU_AIR = MU_AIR / RHO_AIR
ALPHA_AIR = K_AIR / (RHO_AIR * CP_AIR)
PR_AIR = NU_AIR / ALPHA_AIR


# ============================================================
#  EXACT SHABANY-TYPE VIEW FACTOR FUNCTIONS
# ============================================================

def f14_sh(lbar, hbar):
    """Component view factor F14."""
    l = lbar
    h = hbar
    r = math.sqrt(h**2 + l**2)

    value = (2.0 * h**2) / (math.pi * l) * (
        0.5 * math.log(((h**2 + 1.0) * (h**2 + l**2)) /
                       ((h**2 + l**2 + 1.0) * h**2))
        + (r / h**2) * math.atan(1.0 / r)
        + (l * math.sqrt(1.0 + h**2) / h**2) * math.atan(l / math.sqrt(1.0 + h**2))
        - (1.0 / h) * math.atan(1.0 / h)
        - (l / h) * math.atan(l / h)
    )
    return value


def f15_sh(lbar, hbar):
    """Component view factor F15."""
    l = lbar
    h = hbar
    r = math.sqrt(h**2 + l**2)

    tlog = (
        math.log(((1.0 + l**2) * (1.0 + h**2)) / (h**2 + l**2 + 1.0))
        + l**2 * math.log((l**2 * (h**2 + l**2 + 1.0)) /
                          ((h**2 + l**2) * (l**2 + 1.0)))
        + h**2 * math.log((h**2 * (h**2 + l**2 + 1.0)) /
                          ((h**2 + 1.0) * (h**2 + l**2)))
    )

    value = (1.0 / (math.pi * l)) * (
        l * math.atan(1.0 / l)
        + h * math.atan(1.0 / h)
        - r * math.atan(1.0 / r)
        + 0.25 * tlog
    )
    return value


def f24_sh(lbar, hbar):
    """Component view factor F24."""
    l = lbar
    h = hbar
    hp = math.sqrt(1.0 + h**2)

    tlog = (
        math.log(((h**2 + l**2) * (1.0 + l**2)) /
                 ((h**2 + l**2 + 1.0) * l**2))
        + (h**2 / l**2) * math.log((h**2 * (h**2 + l**2 + 1.0)) /
                                   ((h**2 + l**2) * (h**2 + 1.0)))
        + (1.0 / l**2) * math.log((h**2 + l**2 + 1.0) /
                                  ((l**2 + 1.0) * (h**2 + 1.0)))
    )

    value = (l / (math.pi * h)) * (
        (h / l) * math.atan(l / h)
        + (1.0 / l) * math.atan(l)
        - (hp / l) * math.atan(l / hp)
        + 0.25 * tlog
    )
    return value


def f25_sh(lbar, hbar):
    """Component view factor F25."""
    l = lbar
    h = hbar
    lp = math.sqrt(1.0 + l**2)

    tlog = (
        math.log(((l**2 + h**2) * (h**2 + 1.0)) /
                 ((h**2 + l**2 + 1.0) * h**2))
        + (l**2 / h**2) * math.log((l**2 * (h**2 + l**2 + 1.0)) /
                                   ((h**2 + l**2) * (l**2 + 1.0)))
        + (1.0 / h**2) * math.log((h**2 + l**2 + 1.0) /
                                  ((h**2 + 1.0) * (l**2 + 1.0)))
    )

    value = (h / (math.pi * l)) * (
        (l / h) * math.atan(h / l)
        + (1.0 / h) * math.atan(h)
        - (lp / h) * math.atan(h / lp)
        + 0.25 * tlog
    )
    return value


def fs_exact_shabany(lbar, hbar):
    """
    Exact Shabany-type channel-to-surroundings radiation factor.

    Inputs
    ------
    lbar = channel length / fin gap
    hbar = fin height / fin gap

    Returns
    -------
    Fs = effective channel radiation factor
    """
    f14 = f14_sh(lbar, hbar)
    f15 = f15_sh(lbar, hbar)
    f24 = f24_sh(lbar, hbar)
    f25 = f25_sh(lbar, hbar)

    fs = (f14 + 2.0 * f15 + 2.0 * hbar * (f24 + 2.0 * f25)) / (1.0 + 2.0 * hbar)
    return fs


# ============================================================
#  HEAT TRANSFER CORRELATIONS
# ============================================================

def elenbaas_channel_h(delta_t, gap, gravity_length):
    """
    Natural convection coefficient inside vertical plate-fin channels
    using Elenbaas-type modified Rayleigh number.

    gap            : fin spacing [m]
    gravity_length : channel dimension aligned with gravity [m]
    """
    if delta_t <= 0.0:
        return 0.0, 0.0, 0.0

    t_film_k = 273.15 + 25.0 + 0.5 * delta_t
    beta = 1.0 / t_film_k

    ra_star = (
        G * beta * delta_t * gap**3 / (NU_AIR * ALPHA_AIR)
    ) * (gap / gravity_length)

    if ra_star <= 0.0:
        return 0.0, 0.0, 0.0

    nu_channel = (ra_star / 24.0) * (1.0 - math.exp(-35.0 / ra_star))**0.75
    h_channel = nu_channel * K_AIR / gap

    return h_channel, nu_channel, ra_star


def churchill_chu_vertical_h(delta_t, char_length):
    """
    Churchill-Chu natural convection coefficient for exposed vertical surfaces.
    """
    if delta_t <= 0.0:
        return 0.0, 0.0, 0.0

    t_film_k = 273.15 + 25.0 + 0.5 * delta_t
    beta = 1.0 / t_film_k

    ra = G * beta * delta_t * char_length**3 / (NU_AIR * ALPHA_AIR)

    if ra <= 0.0:
        return 0.0, 0.0, 0.0

    nu = 0.68 + (
        0.670 * ra**0.25
    ) / (
        (1.0 + (0.492 / PR_AIR)**(9.0 / 16.0))**(4.0 / 9.0)
    )

    h = nu * K_AIR / char_length

    return h, nu, ra


def gray_body_radiation_q(area, emissivity, ts_k, tsur_k):
    """
    Simple exposed-surface gray-body radiation to large surroundings.
    """
    return emissivity * SIGMA * area * (ts_k**4 - tsur_k**4)


def shabany_channel_radiation_q(area_channel, emissivity, fs, ts_k, tsur_k):
    """
    Open-channel radiation using exact Shabany channel factor Fs.

    Receiver is treated as large surroundings.
    No radome/finite receiver resistance term is used.
    """
    denominator = ((1.0 - emissivity) / emissivity) + (1.0 / fs)
    q = SIGMA * area_channel * (ts_k**4 - tsur_k**4) / denominator
    return q


# ============================================================
#  GEOMETRY AND MODEL
# ============================================================

def run_passive_case(geometry, ts_c, tsur_c, emissivity, orientation_name, gravity_length):
    """
    Calculate passive heat rejection for one geometry, surface temperature,
    surroundings temperature, emissivity, and orientation.
    """

    width = geometry["width_m"]
    length = geometry["length_m"]
    fin_height = geometry["fin_height_m"]
    fin_thickness = geometry["fin_thickness_m"]
    gap = geometry["gap_m"]

    pitch = fin_thickness + gap
    n_fins = int((width + gap) / pitch)
    n_channels = max(n_fins - 1, 1)

    ts_k = ts_c + 273.15
    tsur_k = tsur_c + 273.15
    delta_t = ts_c - tsur_c

    # Channel geometry
    area_one_channel = (gap + 2.0 * fin_height) * length
    area_channel_total = n_channels * area_one_channel

    lbar = length / gap
    hbar = fin_height / gap
    fs = fs_exact_shabany(lbar, hbar)

    # Channel natural convection: channel walls + base between fins
    # Same area as grouped channel area for screening.
    h_ch, nu_ch, ra_star = elenbaas_channel_h(delta_t, gap, gravity_length)
    q_conv_channel = h_ch * area_channel_total * delta_t

    # Channel radiation using exact Shabany factor
    q_rad_channel = shabany_channel_radiation_q(
        area_channel_total, emissivity, fs, ts_k, tsur_k
    )

    # Exposed surfaces
    # Fin tips
    area_fin_tips = n_fins * fin_thickness * length

    # Two outer side faces of outer fins
    area_outer_sides = 2.0 * fin_height * length

    # Two end faces of fin array, approximate exposed area
    area_end_faces = 2.0 * width * fin_height

    # Important: bottom base surface is excluded.
    area_exposed = area_fin_tips + area_outer_sides + area_end_faces

    # Exposed natural convection with Churchill-Chu
    # Use fin height as characteristic vertical length for exposed fin surfaces.
    h_exp, nu_exp, ra_exp = churchill_chu_vertical_h(delta_t, fin_height)
    q_conv_exposed = h_exp * area_exposed * delta_t

    # Exposed radiation
    q_rad_exposed = gray_body_radiation_q(area_exposed, emissivity, ts_k, tsur_k)

    q_total = q_conv_channel + q_rad_channel + q_conv_exposed + q_rad_exposed

    return {
        "geometry": geometry["name"],
        "orientation": orientation_name,
        "Ts_C": ts_c,
        "Tsur_C": tsur_c,
        "epsilon": emissivity,
        "n_fins": n_fins,
        "n_channels": n_channels,
        "Lbar": lbar,
        "Hbar": hbar,
        "Fs": fs,
        "h_ch_W_m2K": h_ch,
        "Nu_ch": nu_ch,
        "Ra_star": ra_star,
        "h_exp_W_m2K": h_exp,
        "Nu_exp": nu_exp,
        "Ra_exp": ra_exp,
        "A_channel_m2": area_channel_total,
        "A_exposed_m2": area_exposed,
        "Q_conv_channel_W": q_conv_channel,
        "Q_rad_channel_W": q_rad_channel,
        "Q_conv_exposed_W": q_conv_exposed,
        "Q_rad_exposed_W": q_rad_exposed,
        "Q_total_W": q_total,
        "status": "PASS" if q_total >= 250.0 else "FAIL",
    }


def main():
    chip_power_w = 250.0

    geometries = [
        {
            "name": "Compact baseline 80x80x25mm",
            "width_m": 80e-3,
            "length_m": 80e-3,
            "base_thickness_m": 5e-3,
            "fin_height_m": 25e-3,
            "fin_thickness_m": 1e-3,
            "gap_m": 2e-3,
        },
        {
            "name": "Larger candidate 80x100x50mm",
            "width_m": 80e-3,
            "length_m": 100e-3,
            "base_thickness_m": 5e-3,
            "fin_height_m": 50e-3,
            "fin_thickness_m": 1e-3,
            "gap_m": 2e-3,
        },
    ]

    surface_temperatures_c = [60.0, 70.0, 85.0, 100.0, 120.0]
    surrounding_temperatures_c = [25.0, 40.0, 50.0]

    emissivity_cases = {
        "bare_aluminum": 0.20,
        "treated_or_oxidized_aluminum": 0.50,
        "black_anodized_aluminum": 0.85,
    }

    all_results = []

    for geometry in geometries:
        fin_height = geometry["fin_height_m"]
        length = geometry["length_m"]

        orientation_cases = {
            "best_vertical_channel_Hf_aligned": fin_height,
            "length_aligned_channel_L_aligned": length,
        }

        for orientation_name, gravity_length in orientation_cases.items():
            for ts_c in surface_temperatures_c:
                for tsur_c in surrounding_temperatures_c:
                    if ts_c <= tsur_c:
                        continue

                    for emissivity_name, emissivity in emissivity_cases.items():
                        result = run_passive_case(
                            geometry=geometry,
                            ts_c=ts_c,
                            tsur_c=tsur_c,
                            emissivity=emissivity,
                            orientation_name=orientation_name,
                            gravity_length=gravity_length,
                        )
                        result["emissivity_case"] = emissivity_name
                        result["chip_power_W"] = chip_power_w
                        all_results.append(result)

    # Create results folder
    os.makedirs("results", exist_ok=True)

    output_file = os.path.join("results", "passive_fanless_heatsink_model.csv")

    fieldnames = list(all_results[0].keys())

    with open(output_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    # Print focused summary at Ts = 85 C and black anodized case
    print("\nPassive / fanless heatsink screening")
    print("=" * 90)
    print(f"Chip heat load target: {chip_power_w:.1f} W")
    print("Bottom heatsink surface is excluded from convection/radiation.")
    print("Channel radiation uses exact Shabany Fs.")
    print("No radome finite-receiver term is used.")
    print("-" * 90)

    print(
        f"{'Geometry':35s} {'Orientation':32s} {'Tsur':>6s} "
        f"{'eps':>5s} {'Fs':>7s} {'Qconv_ch':>10s} {'Qrad_ch':>10s} "
        f"{'Qconv_exp':>10s} {'Qrad_exp':>10s} {'Qtotal':>10s} {'Status':>8s}"
    )
    print("-" * 150)

    for r in all_results:
        if (
            abs(r["Ts_C"] - 85.0) < 1e-9
            and r["emissivity_case"] == "black_anodized_aluminum"
        ):
            print(
                f"{r['geometry'][:35]:35s} "
                f"{r['orientation'][:32]:32s} "
                f"{r['Tsur_C']:6.1f} "
                f"{r['epsilon']:5.2f} "
                f"{r['Fs']:7.4f} "
                f"{r['Q_conv_channel_W']:10.1f} "
                f"{r['Q_rad_channel_W']:10.1f} "
                f"{r['Q_conv_exposed_W']:10.1f} "
                f"{r['Q_rad_exposed_W']:10.1f} "
                f"{r['Q_total_W']:10.1f} "
                f"{r['status']:>8s}"
            )

    print("-" * 90)
    print(f"Full CSV saved to: {output_file}")
    print("\nInterpretation:")
    print("- If Qtotal is far below 250 W at Ts = 85 C, passive/fanless cooling fails.")
    print("- Open ambient is represented by Tsur = 25 C.")
    print("- Warm cabinet is represented by Tsur = 40 C and 50 C.")
    print("- Radiation from the bottom contact surface is not included.")


if __name__ == "__main__":
    main()