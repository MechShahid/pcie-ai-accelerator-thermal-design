"""
Plot high-resolution figures for the PCIe AI accelerator heatsink study.

This script reads:
- results/heatsink_analytical_model.csv
- results/heatsink_design_sweep_robust_pass_both.csv

and saves high-resolution PNG figures in:
- figures/

Purpose:
These plots are for engineering understanding first.
Final GitHub/report formatting can be done later.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. Paths
# ------------------------------------------------------------

baseline_csv = os.path.join("results", "heatsink_analytical_model.csv")
robust_csv = os.path.join("results", "heatsink_design_sweep_robust_pass_both.csv")

figures_dir = "figures"
os.makedirs(figures_dir, exist_ok=True)

# ------------------------------------------------------------
# 2. Read data
# ------------------------------------------------------------

baseline = pd.read_csv(baseline_csv)
robust = pd.read_csv(robust_csv)

# ------------------------------------------------------------
# 3. General plot settings
# ------------------------------------------------------------

plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["font.size"] = 11

TARGET_TCHIP_C = 85.0

# ------------------------------------------------------------
# 4. Baseline: chip temperature vs velocity
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    baseline["V_channel_m_s"],
    baseline["Tchip_teertstra_C"],
    marker="o",
    linewidth=2,
    label="Teertstra-style model",
)

plt.plot(
    baseline["V_channel_m_s"],
    baseline["Tchip_reference_C"],
    marker="s",
    linewidth=2,
    label="Reference Nu = 7.54",
)

plt.axhline(
    TARGET_TCHIP_C,
    linestyle="--",
    linewidth=1.5,
    label="Target 85°C",
)

plt.xlabel("Channel velocity, m/s")
plt.ylabel("Predicted chip temperature, °C")
plt.title("Baseline heatsink chip temperature vs channel velocity")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

path = os.path.join(figures_dir, "baseline_tchip_vs_velocity.png")
plt.savefig(path, dpi=300, bbox_inches="tight")
plt.close()

# ------------------------------------------------------------
# 5. Baseline: heatsink resistance vs velocity
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    baseline["V_channel_m_s"],
    baseline["Rhs_teertstra_K_W"],
    marker="o",
    linewidth=2,
    label="Teertstra-style model",
)

plt.plot(
    baseline["V_channel_m_s"],
    baseline["Rhs_reference_K_W"],
    marker="s",
    linewidth=2,
    label="Reference Nu = 7.54",
)

plt.xlabel("Channel velocity, m/s")
plt.ylabel("Heatsink thermal resistance, K/W")
plt.title("Baseline heatsink resistance vs channel velocity")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

path = os.path.join(figures_dir, "baseline_rhs_vs_velocity.png")
plt.savefig(path, dpi=300, bbox_inches="tight")
plt.close()

# ------------------------------------------------------------
# 6. Robust candidates: Teertstra chip temperature vs CFM
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    robust["volumetric_flow_CFM"],
    robust["T_chip_teertstra_C"],
    s=45,
    alpha=0.8,
)

plt.axhline(
    TARGET_TCHIP_C,
    linestyle="--",
    linewidth=1.5,
    label="Target 85°C",
)

plt.xlabel("Flow through fin channels, CFM")
plt.ylabel("Teertstra-style chip temperature, °C")
plt.title("Robust pass-both candidates: chip temperature vs airflow")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

path = os.path.join(figures_dir, "robust_cfm_vs_tchip.png")
plt.savefig(path, dpi=300, bbox_inches="tight")
plt.close()

# ------------------------------------------------------------
# 7. Robust candidates: conservative margin vs CFM
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    robust["volumetric_flow_CFM"],
    robust["margin_teertstra_C"],
    s=45,
    alpha=0.8,
)

plt.axhline(
    0.0,
    linestyle="--",
    linewidth=1.5,
    label="Zero margin",
)

plt.xlabel("Flow through fin channels, CFM")
plt.ylabel("Conservative thermal margin, °C")
plt.title("Robust pass-both candidates: thermal margin vs airflow")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

path = os.path.join(figures_dir, "robust_margin_vs_cfm.png")
plt.savefig(path, dpi=300, bbox_inches="tight")
plt.close()

# ------------------------------------------------------------
# 8. Top robust candidates only
# ------------------------------------------------------------

top_robust = robust.sort_values(
    by=[
        "V_channel_m_s",
        "Hf_mm",
        "L_mm",
        "b_mm",
        "T_chip_teertstra_C",
    ]
).head(20).copy()

top_robust["design_label"] = (
    "V"
    + top_robust["V_channel_m_s"].astype(str)
    + "_H"
    + top_robust["Hf_mm"].astype(int).astype(str)
    + "_g"
    + top_robust["b_mm"].astype(int).astype(str)
    + "_L"
    + top_robust["L_mm"].astype(int).astype(str)
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_robust["design_label"],
    top_robust["T_chip_teertstra_C"],
)

plt.axvline(
    TARGET_TCHIP_C,
    linestyle="--",
    linewidth=1.5,
    label="Target 85°C",
)

plt.xlabel("Teertstra-style chip temperature, °C")
plt.ylabel("Design candidate")
plt.title("Top robust pass-both candidates")
plt.grid(True, axis="x", alpha=0.3)
plt.legend()
plt.tight_layout()

path = os.path.join(figures_dir, "top_robust_candidates_tchip.png")
plt.savefig(path, dpi=300, bbox_inches="tight")
plt.close()

# ------------------------------------------------------------
# 9. Recommended candidate marker plot
# ------------------------------------------------------------

recommended = robust[
    (robust["V_channel_m_s"] == 5.0)
    & (robust["Hf_mm"] == 50)
    & (robust["b_mm"] == 2)
    & (robust["L_mm"] == 100)
]

plt.figure(figsize=(8, 5))

plt.scatter(
    robust["volumetric_flow_CFM"],
    robust["T_chip_teertstra_C"],
    s=40,
    alpha=0.5,
    label="Robust candidates",
)

if len(recommended) > 0:
    plt.scatter(
        recommended["volumetric_flow_CFM"],
        recommended["T_chip_teertstra_C"],
        s=120,
        marker="*",
        label="Recommended candidate",
    )

plt.axhline(
    TARGET_TCHIP_C,
    linestyle="--",
    linewidth=1.5,
    label="Target 85°C",
)

plt.xlabel("Flow through fin channels, CFM")
plt.ylabel("Teertstra-style chip temperature, °C")
plt.title("Recommended design within robust candidate space")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

path = os.path.join(figures_dir, "recommended_candidate_location.png")
plt.savefig(path, dpi=300, bbox_inches="tight")
plt.close()

# ------------------------------------------------------------
# 10. Print saved files
# ------------------------------------------------------------

print("============================================================")
print("High-resolution figures saved")
print("============================================================")
print(os.path.join(figures_dir, "baseline_tchip_vs_velocity.png"))
print(os.path.join(figures_dir, "baseline_rhs_vs_velocity.png"))
print(os.path.join(figures_dir, "robust_cfm_vs_tchip.png"))
print(os.path.join(figures_dir, "robust_margin_vs_cfm.png"))
print(os.path.join(figures_dir, "top_robust_candidates_tchip.png"))
print(os.path.join(figures_dir, "recommended_candidate_location.png"))
print("============================================================")