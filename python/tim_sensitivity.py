"""
TIM sensitivity model for a simplified 250 W PCIe AI accelerator card.

Purpose:
Study how TIM bond-line thickness and thermal conductivity affect
TIM thermal resistance and estimated chip temperature.

This script also saves the results to:
results/tim_sensitivity.csv
"""

import csv
import os

# ------------------------------------------------------------
# 1. Baseline design inputs
# ------------------------------------------------------------

T_air_inlet_C = 25.0
T_chip_target_C = 85.0
Q_chip_W = 250.0

chip_length_m = 45e-3
chip_width_m = 45e-3
A_chip_m2 = chip_length_m * chip_width_m

# Assumed non-TIM thermal resistance.
# This is still a placeholder and will be replaced later by an
# airflow-dependent analytical heatsink model.
R_non_TIM_K_W = 0.18

# TIM cases: thickness in mm, conductivity in W/mK
tim_cases = [
    ("Thin low-k TIM", 0.1, 3.0),
    ("Baseline TIM", 0.2, 6.0),
    ("Thick high-k TIM", 0.5, 8.0),
    ("Degraded thick TIM", 0.5, 3.0),
    ("High-performance thin TIM", 0.1, 8.0),
]

# ------------------------------------------------------------
# 2. Required thermal resistance
# ------------------------------------------------------------

R_required_K_W = (T_chip_target_C - T_air_inlet_C) / Q_chip_W

# ------------------------------------------------------------
# 3. Sensitivity calculation
# ------------------------------------------------------------

results = []

for case_name, t_TIM_mm, k_TIM_W_mK in tim_cases:
    t_TIM_m = t_TIM_mm * 1e-3

    R_TIM_K_W = t_TIM_m / (k_TIM_W_mK * A_chip_m2)
    R_total_K_W = R_TIM_K_W + R_non_TIM_K_W
    T_chip_C = T_air_inlet_C + Q_chip_W * R_total_K_W
    margin_C = T_chip_target_C - T_chip_C

    status = "PASS" if T_chip_C <= T_chip_target_C else "FAIL"

    results.append({
        "case": case_name,
        "t_TIM_mm": t_TIM_mm,
        "k_TIM_W_mK": k_TIM_W_mK,
        "R_TIM_K_W": R_TIM_K_W,
        "R_total_K_W": R_total_K_W,
        "T_chip_C": T_chip_C,
        "thermal_margin_C": margin_C,
        "status": status,
    })

# ------------------------------------------------------------
# 4. Print results
# ------------------------------------------------------------

print("============================================================")
print("TIM Sensitivity Study")
print("============================================================")
print(f"Chip power                     : {Q_chip_W:.1f} W")
print(f"Inlet air temperature          : {T_air_inlet_C:.1f} degC")
print(f"Target chip temperature        : {T_chip_target_C:.1f} degC")
print(f"Required chip-to-air Rth       : {R_required_K_W:.3f} K/W")
print(f"Chip contact area              : {A_chip_m2:.6f} m^2")
print(f"Assumed non-TIM Rth            : {R_non_TIM_K_W:.3f} K/W")
print("------------------------------------------------------------")

print(
    f"{'Case':<28}"
    f"{'t_TIM [mm]':>12}"
    f"{'k_TIM [W/mK]':>15}"
    f"{'R_TIM [K/W]':>15}"
    f"{'R_total [K/W]':>17}"
    f"{'T_chip [degC]':>17}"
    f"{'Margin [C]':>13}"
    f"{'Status':>10}"
)

print("------------------------------------------------------------")

for row in results:
    print(
        f"{row['case']:<28}"
        f"{row['t_TIM_mm']:>12.3f}"
        f"{row['k_TIM_W_mK']:>15.1f}"
        f"{row['R_TIM_K_W']:>15.4f}"
        f"{row['R_total_K_W']:>17.4f}"
        f"{row['T_chip_C']:>17.1f}"
        f"{row['thermal_margin_C']:>13.1f}"
        f"{row['status']:>10}"
    )

print("============================================================")

# ------------------------------------------------------------
# 5. Save CSV results
# ------------------------------------------------------------

os.makedirs("results", exist_ok=True)

csv_path = os.path.join("results", "tim_sensitivity.csv")

with open(csv_path, mode="w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "case",
            "t_TIM_mm",
            "k_TIM_W_mK",
            "R_TIM_K_W",
            "R_total_K_W",
            "T_chip_C",
            "thermal_margin_C",
            "status",
        ],
    )
    writer.writeheader()
    writer.writerows(results)

print(f"CSV results saved to: {csv_path}")