"""
Single-stream heat-exchanger model for a forced-air plate-fin heatsink.

Project:
Simplified thermal design study of a 250 W PCIe AI accelerator card.

Purpose:
Treat the forced-air heatsink as a single-stream compact heat exchanger.

This script compares two analytical estimates:

1. Teertstra-style developing-flow estimate
2. Reference fully developed laminar estimate using Nu = 7.54

The comparison helps check whether the conclusion depends strongly on one
correlation. If both estimates fail, the design conclusion is stronger.

Main heat-exchanger relations:

    NTU = h A_eff / (m_dot cp)
    epsilon = 1 - exp(-NTU)
    R_hs = 1 / (m_dot cp epsilon)

Important assumptions:
- Guided/ducted flow through fin channels
- Straight plate-fin aluminum heatsink
- Air only, single-stream heat exchanger
- Steady-state forced convection
- Fin efficiency included
- No bypass flow, recirculation, fan swirl, radiation, or detailed spreading
- CFD is still required later for 3D flow, pressure drop, and component coupling
"""

import csv
import math
import os

# ------------------------------------------------------------
# 1. Thermal targets and heat loads
# ------------------------------------------------------------

T_air_inlet_C = 25.0
T_chip_target_C = 85.0

Q_chip_W = 250.0
Q_full_board_W = 320.0

# ------------------------------------------------------------
# 2. Air properties near room temperature
# ------------------------------------------------------------

rho_air_kg_m3 = 1.184
cp_air_J_kgK = 1007.0
mu_air_Pa_s = 1.85e-5
k_air_W_mK = 0.0263

Pr_air = cp_air_J_kgK * mu_air_Pa_s / k_air_W_mK

# ------------------------------------------------------------
# 3. Heatsink geometry
# ------------------------------------------------------------

L_m = 80e-3          # flow length
W_m = 80e-3          # width across fins
base_thickness_m = 5e-3

Hf_m = 25e-3         # fin height
tf_m = 1e-3          # fin thickness
b_m = 2e-3           # fin gap / spacing

k_fin_W_mK = 180.0
k_base_W_mK = 180.0

pitch_m = tf_m + b_m
number_of_fins = int(W_m / pitch_m)
number_of_channels = max(number_of_fins - 1, 1)

used_width_m = number_of_fins * tf_m + number_of_channels * b_m

single_channel_area_m2 = b_m * Hf_m
total_channel_flow_area_m2 = number_of_channels * single_channel_area_m2

D_h_m = 2.0 * b_m * Hf_m / (b_m + Hf_m)

fin_side_area_m2 = number_of_fins * 2.0 * L_m * Hf_m
base_exposed_area_m2 = number_of_channels * b_m * L_m
total_geometric_area_m2 = fin_side_area_m2 + base_exposed_area_m2

# ------------------------------------------------------------
# 4. Chip and TIM
# ------------------------------------------------------------

chip_length_m = 45e-3
chip_width_m = 45e-3
A_chip_m2 = chip_length_m * chip_width_m

t_TIM_m = 0.2e-3
k_TIM_W_mK = 6.0

R_TIM_K_W = t_TIM_m / (k_TIM_W_mK * A_chip_m2)

# Placeholder for spreading/contact/base resistance
R_spreading_contact_base_K_W = 0.03

# ------------------------------------------------------------
# 5. Airflow cases
# ------------------------------------------------------------

velocity_cases_m_s = [1.0, 2.0, 3.0, 4.0]

# ------------------------------------------------------------
# 6. Helper functions
# ------------------------------------------------------------

def safe_divide(numerator, denominator):
    if abs(denominator) < 1e-30:
        return float("inf")
    return numerator / denominator


def classify_reynolds_number(Re_Dh):
    if Re_Dh < 2300.0:
        return "Laminar indicator"
    elif Re_Dh < 4000.0:
        return "Transitional indicator"
    else:
        return "Turbulent indicator"


def classify_temperature(T_chip_C):
    if T_chip_C <= T_chip_target_C:
        return "PASS"
    return "FAIL"


def teertstra_style_nusselt(V_channel_m_s):
    """
    Approximate developing-flow plate-fin / parallel-plate Nusselt estimate.

    Uses:
        Re_b = rho V b / mu
        Re_star = Re_b * b / L

    This is a screening model, not final validation.
    """

    Re_b = rho_air_kg_m3 * V_channel_m_s * b_m / mu_air_Pa_s
    Re_star = Re_b * b_m / L_m
    Re_star = max(Re_star, 1e-12)

    term_developing = (
        0.664
        * math.sqrt(Re_star)
        * (Pr_air ** (1.0 / 3.0))
        * (1.0 + 3.65 / math.sqrt(Re_star)) ** 0.5
    )

    term_fully_developed = Re_star * Pr_air / 2.0

    Nu_ideal = (
        (term_fully_developed ** -3.0)
        + (term_developing ** -3.0)
    ) ** (-1.0 / 3.0)

    return Nu_ideal, Re_b, Re_star


def fin_efficiency(h_W_m2K):
    """
    Straight rectangular fin efficiency with adiabatic tip approximation.

        eta = tanh(m Hf) / (m Hf)

    where:

        m = sqrt(2h / (k_fin tf))
    """

    m_inv_m = math.sqrt(2.0 * h_W_m2K / (k_fin_W_mK * tf_m))
    mH = m_inv_m * Hf_m

    if mH < 1e-12:
        return 1.0

    return math.tanh(mH) / mH


def heat_exchanger_result(Nu, C_air_W_K):
    """
    Calculate h, fin efficiency, effective area, NTU, epsilon,
    heatsink resistance, total resistance, and chip temperature
    for a given Nusselt number.
    """

    h_W_m2K = Nu * k_air_W_mK / b_m

    eta = fin_efficiency(h_W_m2K)

    A_eff_m2 = base_exposed_area_m2 + eta * fin_side_area_m2

    hA_eff_W_K = h_W_m2K * A_eff_m2

    NTU = safe_divide(hA_eff_W_K, C_air_W_K)

    epsilon = 1.0 - math.exp(-NTU)

    R_hs_K_W = safe_divide(1.0, C_air_W_K * epsilon)

    R_conv_simple_K_W = safe_divide(1.0, hA_eff_W_K)

    R_total_K_W = (
        R_TIM_K_W
        + R_spreading_contact_base_K_W
        + R_hs_K_W
    )

    T_chip_C = T_air_inlet_C + Q_chip_W * R_total_K_W

    margin_C = T_chip_target_C - T_chip_C

    return {
        "Nu": Nu,
        "h_W_m2K": h_W_m2K,
        "eta_fin": eta,
        "A_eff_m2": A_eff_m2,
        "hA_eff_W_K": hA_eff_W_K,
        "NTU": NTU,
        "epsilon": epsilon,
        "R_conv_simple_K_W": R_conv_simple_K_W,
        "R_hs_K_W": R_hs_K_W,
        "R_total_K_W": R_total_K_W,
        "T_chip_C": T_chip_C,
        "thermal_margin_C": margin_C,
        "status": classify_temperature(T_chip_C),
    }


# ------------------------------------------------------------
# 7. Main calculation
# ------------------------------------------------------------

results = []

for V_channel_m_s in velocity_cases_m_s:

    volumetric_flow_m3_s = V_channel_m_s * total_channel_flow_area_m2
    volumetric_flow_CFM = volumetric_flow_m3_s * 2118.88
    volumetric_flow_m3_h = volumetric_flow_m3_s * 3600.0

    m_dot_kg_s = rho_air_kg_m3 * volumetric_flow_m3_s
    C_air_W_K = m_dot_kg_s * cp_air_J_kgK

    Re_Dh = rho_air_kg_m3 * V_channel_m_s * D_h_m / mu_air_Pa_s

    Nu_teertstra, Re_b, Re_star = teertstra_style_nusselt(V_channel_m_s)

    Nu_reference = 7.54

    teertstra = heat_exchanger_result(Nu_teertstra, C_air_W_K)
    reference = heat_exchanger_result(Nu_reference, C_air_W_K)

    T_air_out_chip_C = T_air_inlet_C + safe_divide(Q_chip_W, C_air_W_K)
    T_air_out_full_board_C = T_air_inlet_C + safe_divide(Q_full_board_W, C_air_W_K)

    deltaT_air_chip_K = T_air_out_chip_C - T_air_inlet_C
    deltaT_air_full_board_K = T_air_out_full_board_C - T_air_inlet_C

    dynamic_pressure_Pa = 0.5 * rho_air_kg_m3 * V_channel_m_s**2

    friction_factor_Darcy_approx = safe_divide(96.0, Re_Dh)

    pressure_drop_channel_Pa_approx = (
        friction_factor_Darcy_approx
        * (L_m / D_h_m)
        * dynamic_pressure_Pa
    )

    results.append({
        "V_channel_m_s": V_channel_m_s,
        "volumetric_flow_m3_s": volumetric_flow_m3_s,
        "volumetric_flow_CFM": volumetric_flow_CFM,
        "volumetric_flow_m3_h": volumetric_flow_m3_h,
        "m_dot_kg_s": m_dot_kg_s,
        "C_air_W_K": C_air_W_K,
        "Re_Dh": Re_Dh,
        "Re_b": Re_b,
        "Re_star": Re_star,
        "Re_note": classify_reynolds_number(Re_Dh),
        "Pr_air": Pr_air,
        "Nu_teertstra": teertstra["Nu"],
        "h_teertstra_W_m2K": teertstra["h_W_m2K"],
        "eta_teertstra": teertstra["eta_fin"],
        "A_eff_teertstra_m2": teertstra["A_eff_m2"],
        "hA_teertstra_W_K": teertstra["hA_eff_W_K"],
        "NTU_teertstra": teertstra["NTU"],
        "epsilon_teertstra": teertstra["epsilon"],
        "Rhs_teertstra_K_W": teertstra["R_hs_K_W"],
        "Rtotal_teertstra_K_W": teertstra["R_total_K_W"],
        "Tchip_teertstra_C": teertstra["T_chip_C"],
        "margin_teertstra_C": teertstra["thermal_margin_C"],
        "status_teertstra": teertstra["status"],
        "Nu_reference": reference["Nu"],
        "h_reference_W_m2K": reference["h_W_m2K"],
        "eta_reference": reference["eta_fin"],
        "A_eff_reference_m2": reference["A_eff_m2"],
        "hA_reference_W_K": reference["hA_eff_W_K"],
        "NTU_reference": reference["NTU"],
        "epsilon_reference": reference["epsilon"],
        "Rhs_reference_K_W": reference["R_hs_K_W"],
        "Rtotal_reference_K_W": reference["R_total_K_W"],
        "Tchip_reference_C": reference["T_chip_C"],
        "margin_reference_C": reference["thermal_margin_C"],
        "status_reference": reference["status"],
        "T_air_out_chip_C": T_air_out_chip_C,
        "T_air_out_full_board_C": T_air_out_full_board_C,
        "deltaT_air_chip_K": deltaT_air_chip_K,
        "deltaT_air_full_board_K": deltaT_air_full_board_K,
        "dynamic_pressure_Pa": dynamic_pressure_Pa,
        "friction_factor_Darcy_approx": friction_factor_Darcy_approx,
        "pressure_drop_channel_Pa_approx": pressure_drop_channel_Pa_approx,
    })

# ------------------------------------------------------------
# 8. Print summary
# ------------------------------------------------------------

print("============================================================")
print("Single-Stream Heat-Exchanger Model for Forced-Air Heatsink")
print("============================================================")
print(f"Inlet air temperature              : {T_air_inlet_C:.1f} degC")
print(f"Chip heat load                     : {Q_chip_W:.1f} W")
print(f"Full board heat load               : {Q_full_board_W:.1f} W")
print(f"Target chip temperature            : {T_chip_target_C:.1f} degC")
print("------------------------------------------------------------")
print(f"Heatsink length, L                 : {L_m*1e3:.1f} mm")
print(f"Heatsink width, W                  : {W_m*1e3:.1f} mm")
print(f"Base thickness                     : {base_thickness_m*1e3:.1f} mm")
print(f"Fin height, Hf                     : {Hf_m*1e3:.1f} mm")
print(f"Fin thickness, tf                  : {tf_m*1e3:.1f} mm")
print(f"Fin spacing/gap, b                 : {b_m*1e3:.1f} mm")
print(f"Estimated number of fins           : {number_of_fins}")
print(f"Estimated number of channels       : {number_of_channels}")
print(f"Used heatsink width                : {used_width_m*1e3:.1f} mm")
print(f"Hydraulic diameter, Dh             : {D_h_m*1e3:.2f} mm")
print(f"Total channel flow area            : {total_channel_flow_area_m2:.6f} m^2")
print(f"Fin side area                      : {fin_side_area_m2:.6f} m^2")
print(f"Exposed base area                  : {base_exposed_area_m2:.6f} m^2")
print(f"Total geometric area               : {total_geometric_area_m2:.6f} m^2")
print("------------------------------------------------------------")
print(f"TIM resistance                     : {R_TIM_K_W:.4f} K/W")
print(f"Spreading/contact/base placeholder : {R_spreading_contact_base_K_W:.4f} K/W")
print("------------------------------------------------------------")
print("Model comparison:")
print("1. Teertstra-style developing-flow estimate")
print("2. Reference fully developed laminar estimate using Nu = 7.54")
print("============================================================")

header = (
    f"{'Vch':>5}"
    f"{'CFM':>7}"
    f"{'ReDh':>7}"
    f"{'Nu_T':>7}"
    f"{'h_T':>8}"
    f"{'Rhs_T':>8}"
    f"{'Tchip_T':>9}"
    f"{'Nu_ref':>8}"
    f"{'h_ref':>8}"
    f"{'Rhs_ref':>9}"
    f"{'Tchip_ref':>11}"
    f"{'Tout250':>9}"
    f"{'dP~':>8}"
    f"{'T_stat':>8}"
    f"{'Ref_stat':>9}"
)

print(header)
print("-" * len(header))

for row in results:
    print(
        f"{row['V_channel_m_s']:>5.1f}"
        f"{row['volumetric_flow_CFM']:>7.1f}"
        f"{row['Re_Dh']:>7.0f}"
        f"{row['Nu_teertstra']:>7.2f}"
        f"{row['h_teertstra_W_m2K']:>8.1f}"
        f"{row['Rhs_teertstra_K_W']:>8.3f}"
        f"{row['Tchip_teertstra_C']:>9.1f}"
        f"{row['Nu_reference']:>8.2f}"
        f"{row['h_reference_W_m2K']:>8.1f}"
        f"{row['Rhs_reference_K_W']:>9.3f}"
        f"{row['Tchip_reference_C']:>11.1f}"
        f"{row['T_air_out_chip_C']:>9.1f}"
        f"{row['pressure_drop_channel_Pa_approx']:>8.1f}"
        f"{row['status_teertstra']:>8}"
        f"{row['status_reference']:>9}"
    )

print("============================================================")
print("Notes:")
print("- Vch is velocity inside the fin channels.")
print("- T suffix means Teertstra-style model.")
print("- ref suffix means Nu = 7.54 reference model.")
print("- Rhs is single-stream heat-exchanger resistance.")
print("- Tout250 is bulk outlet air temperature for 250 W.")
print("- dP~ is only a rough laminar channel pressure-drop estimate.")
print("- CFD is still needed for bypass, spreading, and pressure drop.")
print("============================================================")

# ------------------------------------------------------------
# 9. Save CSV
# ------------------------------------------------------------

os.makedirs("results", exist_ok=True)

csv_path = os.path.join("results", "heatsink_analytical_model.csv")

with open(csv_path, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=list(results[0].keys()))
    writer.writeheader()
    writer.writerows(results)

print(f"CSV results saved to: {csv_path}")