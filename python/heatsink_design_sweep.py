"""
Design sweep for forced-air plate-fin heatsink.

Project:
Simplified thermal design study of a 250 W PCIe AI accelerator card.

Purpose:
The baseline 80 mm x 80 mm x 25 mm heatsink failed the 85 C chip target.
This script sweeps geometry and airflow to find feasible combinations.

Swept parameters:
- Channel velocity
- Fin height
- Fin gap
- Heatsink length

Model:
Single-stream heat-exchanger model

    NTU = h A_eff / (m_dot cp)
    epsilon = 1 - exp(-NTU)
    R_hs = 1 / (m_dot cp epsilon)

Total chip-to-air resistance:

    R_total = R_TIM + R_spreading/contact/base + R_hs

Chip temperature:

    T_chip = T_air_inlet + Q_chip * R_total

Two models are compared:
1. Teertstra-style developing-flow model
2. Reference fully developed laminar model using Nu = 7.54

The script saves:
- Full sweep results
- All passing results
- Robust results passing BOTH models

Important:
This is an analytical screening model only.
CFD is still needed later for bypass, pressure drop, recirculation,
spreading, and detailed 3D temperature field.
"""

import csv
import math
import os

# ------------------------------------------------------------
# 1. Thermal target
# ------------------------------------------------------------

T_air_inlet_C = 25.0
T_chip_target_C = 85.0

Q_chip_W = 250.0
Q_full_board_W = 320.0

# ------------------------------------------------------------
# 2. Air properties
# ------------------------------------------------------------

rho_air_kg_m3 = 1.184
cp_air_J_kgK = 1007.0
mu_air_Pa_s = 1.85e-5
k_air_W_mK = 0.0263

Pr_air = cp_air_J_kgK * mu_air_Pa_s / k_air_W_mK

# ------------------------------------------------------------
# 3. Fixed heatsink / chip assumptions
# ------------------------------------------------------------

W_m = 80e-3
tf_m = 1e-3
base_thickness_m = 5e-3

k_fin_W_mK = 180.0

chip_length_m = 45e-3
chip_width_m = 45e-3
A_chip_m2 = chip_length_m * chip_width_m

t_TIM_m = 0.2e-3
k_TIM_W_mK = 6.0

R_TIM_K_W = t_TIM_m / (k_TIM_W_mK * A_chip_m2)

# Keep this separate and honest.
R_spreading_contact_base_K_W = 0.03

# ------------------------------------------------------------
# 4. Sweep ranges
# ------------------------------------------------------------

velocity_cases_m_s = [2, 3, 4, 5, 6, 8, 10, 12]
fin_height_cases_mm = [25, 30, 35, 40, 50]
fin_gap_cases_mm = [2, 3, 4, 5]
length_cases_mm = [80, 100, 120, 150]

# ------------------------------------------------------------
# 5. Helper functions
# ------------------------------------------------------------

def safe_divide(numerator, denominator):
    if abs(denominator) < 1e-30:
        return float("inf")
    return numerator / denominator


def classify_temperature(T_chip_C):
    if T_chip_C <= T_chip_target_C:
        return "PASS"
    return "FAIL"


def classify_reynolds_number(Re_Dh):
    if Re_Dh < 2300:
        return "Laminar indicator"
    elif Re_Dh < 4000:
        return "Transitional indicator"
    return "Turbulent indicator"


def teertstra_style_nusselt(V_channel_m_s, b_m, L_m):
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


def fin_efficiency(h_W_m2K, Hf_m):
    """
    Straight rectangular fin efficiency with adiabatic tip approximation.
    """

    m_inv_m = math.sqrt(2.0 * h_W_m2K / (k_fin_W_mK * tf_m))
    mH = m_inv_m * Hf_m

    if mH < 1e-12:
        return 1.0

    return math.tanh(mH) / mH


def calculate_case(V_channel_m_s, Hf_mm, b_mm, L_mm, model_name):
    Hf_m = Hf_mm * 1e-3
    b_m = b_mm * 1e-3
    L_m = L_mm * 1e-3

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

    volumetric_flow_m3_s = V_channel_m_s * total_channel_flow_area_m2
    volumetric_flow_CFM = volumetric_flow_m3_s * 2118.88
    volumetric_flow_m3_h = volumetric_flow_m3_s * 3600.0

    m_dot_kg_s = rho_air_kg_m3 * volumetric_flow_m3_s
    C_air_W_K = m_dot_kg_s * cp_air_J_kgK

    Re_Dh = rho_air_kg_m3 * V_channel_m_s * D_h_m / mu_air_Pa_s

    Nu_teertstra, Re_b, Re_star = teertstra_style_nusselt(
        V_channel_m_s,
        b_m,
        L_m,
    )

    if model_name == "teertstra":
        Nu = Nu_teertstra
    elif model_name == "reference_Nu_7_54":
        Nu = 7.54
    else:
        raise ValueError("Unknown model name")

    h_W_m2K = Nu * k_air_W_mK / b_m

    eta_fin = fin_efficiency(h_W_m2K, Hf_m)

    A_eff_m2 = base_exposed_area_m2 + eta_fin * fin_side_area_m2

    hA_eff_W_K = h_W_m2K * A_eff_m2

    NTU = safe_divide(hA_eff_W_K, C_air_W_K)

    epsilon = 1.0 - math.exp(-NTU)

    R_hs_K_W = safe_divide(1.0, C_air_W_K * epsilon)

    R_total_K_W = (
        R_TIM_K_W
        + R_spreading_contact_base_K_W
        + R_hs_K_W
    )

    T_chip_C = T_air_inlet_C + Q_chip_W * R_total_K_W
    margin_C = T_chip_target_C - T_chip_C

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

    return {
        "model": model_name,
        "V_channel_m_s": V_channel_m_s,
        "Hf_mm": Hf_mm,
        "b_mm": b_mm,
        "L_mm": L_mm,
        "W_mm": W_m * 1e3,
        "tf_mm": tf_m * 1e3,
        "number_of_fins": number_of_fins,
        "number_of_channels": number_of_channels,
        "used_width_mm": used_width_m * 1e3,
        "Dh_mm": D_h_m * 1e3,
        "flow_area_m2": total_channel_flow_area_m2,
        "fin_side_area_m2": fin_side_area_m2,
        "base_exposed_area_m2": base_exposed_area_m2,
        "total_geometric_area_m2": total_geometric_area_m2,
        "volumetric_flow_CFM": volumetric_flow_CFM,
        "volumetric_flow_m3_h": volumetric_flow_m3_h,
        "m_dot_kg_s": m_dot_kg_s,
        "C_air_W_K": C_air_W_K,
        "Re_Dh": Re_Dh,
        "Re_note": classify_reynolds_number(Re_Dh),
        "Re_b": Re_b,
        "Re_star": Re_star,
        "Nu": Nu,
        "h_W_m2K": h_W_m2K,
        "eta_fin": eta_fin,
        "A_eff_m2": A_eff_m2,
        "hA_eff_W_K": hA_eff_W_K,
        "NTU": NTU,
        "epsilon": epsilon,
        "R_TIM_K_W": R_TIM_K_W,
        "R_spreading_contact_base_K_W": R_spreading_contact_base_K_W,
        "R_hs_K_W": R_hs_K_W,
        "R_total_K_W": R_total_K_W,
        "T_chip_C": T_chip_C,
        "thermal_margin_C": margin_C,
        "T_air_out_chip_C": T_air_out_chip_C,
        "T_air_out_full_board_C": T_air_out_full_board_C,
        "deltaT_air_chip_K": deltaT_air_chip_K,
        "deltaT_air_full_board_K": deltaT_air_full_board_K,
        "dynamic_pressure_Pa": dynamic_pressure_Pa,
        "pressure_drop_channel_Pa_approx": pressure_drop_channel_Pa_approx,
        "status": classify_temperature(T_chip_C),
    }


# ------------------------------------------------------------
# 6. Run sweep
# ------------------------------------------------------------

results = []

for model_name in ["teertstra", "reference_Nu_7_54"]:
    for V_channel_m_s in velocity_cases_m_s:
        for Hf_mm in fin_height_cases_mm:
            for b_mm in fin_gap_cases_mm:
                for L_mm in length_cases_mm:
                    result = calculate_case(
                        V_channel_m_s,
                        Hf_mm,
                        b_mm,
                        L_mm,
                        model_name,
                    )
                    results.append(result)

# ------------------------------------------------------------
# 7. Save full results
# ------------------------------------------------------------

os.makedirs("results", exist_ok=True)

full_csv_path = os.path.join("results", "heatsink_design_sweep_full.csv")

with open(full_csv_path, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=list(results[0].keys()))
    writer.writeheader()
    writer.writerows(results)

# ------------------------------------------------------------
# 8. Extract all passing designs
# ------------------------------------------------------------

passing_results = [row for row in results if row["status"] == "PASS"]

passing_csv_path = os.path.join("results", "heatsink_design_sweep_passing.csv")

if passing_results:
    with open(passing_csv_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(passing_results[0].keys()))
        writer.writeheader()
        writer.writerows(passing_results)

# ------------------------------------------------------------
# 9. Extract robust designs passing BOTH models
# ------------------------------------------------------------

grouped_cases = {}

for row in results:
    key = (
        row["V_channel_m_s"],
        row["Hf_mm"],
        row["b_mm"],
        row["L_mm"],
    )

    if key not in grouped_cases:
        grouped_cases[key] = {}

    grouped_cases[key][row["model"]] = row


robust_results = []

for key, model_rows in grouped_cases.items():

    if "teertstra" not in model_rows:
        continue

    if "reference_Nu_7_54" not in model_rows:
        continue

    teertstra_row = model_rows["teertstra"]
    reference_row = model_rows["reference_Nu_7_54"]

    if (
        teertstra_row["status"] == "PASS"
        and reference_row["status"] == "PASS"
    ):
        robust_results.append({
            "V_channel_m_s": teertstra_row["V_channel_m_s"],
            "Hf_mm": teertstra_row["Hf_mm"],
            "b_mm": teertstra_row["b_mm"],
            "L_mm": teertstra_row["L_mm"],
            "W_mm": teertstra_row["W_mm"],
            "tf_mm": teertstra_row["tf_mm"],
            "number_of_fins": teertstra_row["number_of_fins"],
            "number_of_channels": teertstra_row["number_of_channels"],
            "used_width_mm": teertstra_row["used_width_mm"],
            "Dh_mm": teertstra_row["Dh_mm"],
            "flow_area_m2": teertstra_row["flow_area_m2"],
            "volumetric_flow_CFM": teertstra_row["volumetric_flow_CFM"],
            "volumetric_flow_m3_h": teertstra_row["volumetric_flow_m3_h"],
            "m_dot_kg_s": teertstra_row["m_dot_kg_s"],
            "C_air_W_K": teertstra_row["C_air_W_K"],
            "Re_Dh": teertstra_row["Re_Dh"],
            "Re_note": teertstra_row["Re_note"],
            "Re_b_teertstra": teertstra_row["Re_b"],
            "Re_star_teertstra": teertstra_row["Re_star"],
            "Nu_teertstra": teertstra_row["Nu"],
            "Nu_reference": reference_row["Nu"],
            "h_teertstra_W_m2K": teertstra_row["h_W_m2K"],
            "h_reference_W_m2K": reference_row["h_W_m2K"],
            "eta_fin_teertstra": teertstra_row["eta_fin"],
            "eta_fin_reference": reference_row["eta_fin"],
            "A_eff_teertstra_m2": teertstra_row["A_eff_m2"],
            "A_eff_reference_m2": reference_row["A_eff_m2"],
            "hA_teertstra_W_K": teertstra_row["hA_eff_W_K"],
            "hA_reference_W_K": reference_row["hA_eff_W_K"],
            "NTU_teertstra": teertstra_row["NTU"],
            "NTU_reference": reference_row["NTU"],
            "epsilon_teertstra": teertstra_row["epsilon"],
            "epsilon_reference": reference_row["epsilon"],
            "R_hs_teertstra_K_W": teertstra_row["R_hs_K_W"],
            "R_hs_reference_K_W": reference_row["R_hs_K_W"],
            "R_total_teertstra_K_W": teertstra_row["R_total_K_W"],
            "R_total_reference_K_W": reference_row["R_total_K_W"],
            "T_chip_teertstra_C": teertstra_row["T_chip_C"],
            "T_chip_reference_C": reference_row["T_chip_C"],
            "margin_teertstra_C": teertstra_row["thermal_margin_C"],
            "margin_reference_C": reference_row["thermal_margin_C"],
            "T_air_out_chip_C": teertstra_row["T_air_out_chip_C"],
            "T_air_out_full_board_C": teertstra_row["T_air_out_full_board_C"],
            "deltaT_air_chip_K": teertstra_row["deltaT_air_chip_K"],
            "deltaT_air_full_board_K": teertstra_row["deltaT_air_full_board_K"],
            "pressure_drop_channel_Pa_approx": teertstra_row[
                "pressure_drop_channel_Pa_approx"
            ],
            "robust_status": "PASS_BOTH",
        })


robust_csv_path = os.path.join(
    "results",
    "heatsink_design_sweep_robust_pass_both.csv",
)

if robust_results:
    with open(robust_csv_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(robust_results[0].keys()))
        writer.writeheader()
        writer.writerows(robust_results)

# ------------------------------------------------------------
# 10. Print summary
# ------------------------------------------------------------

print("============================================================")
print("Heatsink Design Sweep")
print("============================================================")
print(f"Total cases checked                 : {len(results)}")
print(f"Passing cases                       : {len(passing_results)}")
print(f"Robust cases passing both models    : {len(robust_results)}")
print(f"Target chip temperature             : {T_chip_target_C:.1f} degC")
print(f"Inlet air temperature               : {T_air_inlet_C:.1f} degC")
print(f"Chip heat load                      : {Q_chip_W:.1f} W")
print("------------------------------------------------------------")
print(f"Full CSV saved to                   : {full_csv_path}")

if passing_results:
    print(f"Passing CSV saved to                : {passing_csv_path}")

if robust_results:
    print(f"Robust pass-both CSV saved to       : {robust_csv_path}")

# ------------------------------------------------------------
# 11. Print top passing candidates
# ------------------------------------------------------------

if passing_results:
    passing_sorted = sorted(
        passing_results,
        key=lambda row: (
            row["model"],
            row["V_channel_m_s"],
            row["Hf_mm"],
            row["L_mm"],
            -row["thermal_margin_C"],
        ),
    )

    print("------------------------------------------------------------")
    print("Top passing candidates:")
    print(
        f"{'Model':<20}"
        f"{'Vch':>6}"
        f"{'CFM':>8}"
        f"{'Hf':>6}"
        f"{'gap':>6}"
        f"{'L':>6}"
        f"{'fins':>6}"
        f"{'ReDh':>8}"
        f"{'Nu':>8}"
        f"{'Rhs':>8}"
        f"{'Tchip':>9}"
        f"{'Tout':>9}"
        f"{'dP~':>8}"
        f"{'Margin':>9}"
    )
    print("-" * 132)

    for row in passing_sorted[:20]:
        print(
            f"{row['model']:<20}"
            f"{row['V_channel_m_s']:>6.1f}"
            f"{row['volumetric_flow_CFM']:>8.1f}"
            f"{row['Hf_mm']:>6.0f}"
            f"{row['b_mm']:>6.0f}"
            f"{row['L_mm']:>6.0f}"
            f"{row['number_of_fins']:>6}"
            f"{row['Re_Dh']:>8.0f}"
            f"{row['Nu']:>8.2f}"
            f"{row['R_hs_K_W']:>8.3f}"
            f"{row['T_chip_C']:>9.1f}"
            f"{row['T_air_out_chip_C']:>9.1f}"
            f"{row['pressure_drop_channel_Pa_approx']:>8.1f}"
            f"{row['thermal_margin_C']:>9.1f}"
        )
else:
    print("No passing cases found in this sweep.")
    print("Increase velocity, heatsink size, fin height, or reduce heat load.")

# ------------------------------------------------------------
# 12. Print robust candidates
# ------------------------------------------------------------

if robust_results:
    robust_sorted = sorted(
        robust_results,
        key=lambda row: (
            row["V_channel_m_s"],
            row["Hf_mm"],
            row["L_mm"],
            -row["margin_teertstra_C"],
        ),
    )

    print("------------------------------------------------------------")
    print("Top robust candidates passing BOTH models:")
    print(
        f"{'Vch':>6}"
        f"{'CFM':>8}"
        f"{'Hf':>6}"
        f"{'gap':>6}"
        f"{'L':>6}"
        f"{'fins':>6}"
        f"{'ReDh':>8}"
        f"{'Tchip_T':>10}"
        f"{'Tchip_ref':>11}"
        f"{'Tout':>9}"
        f"{'dP~':>8}"
        f"{'Margin_T':>10}"
    )
    print("-" * 106)

    for row in robust_sorted[:20]:
        print(
            f"{row['V_channel_m_s']:>6.1f}"
            f"{row['volumetric_flow_CFM']:>8.1f}"
            f"{row['Hf_mm']:>6.0f}"
            f"{row['b_mm']:>6.0f}"
            f"{row['L_mm']:>6.0f}"
            f"{row['number_of_fins']:>6}"
            f"{row['Re_Dh']:>8.0f}"
            f"{row['T_chip_teertstra_C']:>10.1f}"
            f"{row['T_chip_reference_C']:>11.1f}"
            f"{row['T_air_out_chip_C']:>9.1f}"
            f"{row['pressure_drop_channel_Pa_approx']:>8.1f}"
            f"{row['margin_teertstra_C']:>10.1f}"
        )
else:
    print("------------------------------------------------------------")
    print("No robust candidates passed both models.")
    print("The passing cases are optimistic/reference-only designs.")

print("============================================================")