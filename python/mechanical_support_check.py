# mechanical_support_check.py
# Concept-level mechanical support screening for PCIe AI accelerator heatsink
# This is NOT a full structural validation, PCIe compliance check, or shock/vibration analysis.

import math
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures"

RESULTS_DIR.mkdir(exist_ok=True)
FIGURES_DIR.mkdir(exist_ok=True)


# ============================================================
# 2. CONSTANTS
# ============================================================

ALUMINIUM_DENSITY_KG_M3 = 2700.0
GRAVITY_M_S2 = 9.81

# Simple concept-level screening thresholds
LOW_SUPPORT_RISK_MASS_G = 250.0
MEDIUM_SUPPORT_RISK_MASS_G = 350.0

# Approximate lever arm from PCB/support load path to heatsink centre of gravity.
# This is a screening assumption, not a detailed structural model.
LEVER_ARM_MM = 35.0


# ============================================================
# 3. HEATSINK CASE DEFINITIONS
# ============================================================

cases = [
    {
        "case": "CFD-0 reference",
        "description": "80 x 100 x 50 mm reference heatsink",
        "base_width_mm": 80.0,
        "base_length_mm": 100.0,
        "base_thickness_mm": 5.0,
        "fin_height_mm": 50.0,
        "fin_length_mm": 100.0,
        "fin_thickness_mm": 1.0,
        "number_of_fins": 26,
        "thermal_result": "Pass",
        "max_chip_temperature_C": 75.97,
        "pressure_drop_Pa": 28.8,
    },
    {
        "case": "CFD-1 reduced-height open/bypass",
        "description": "80 x 100 x 35 mm open/bypass heatsink",
        "base_width_mm": 80.0,
        "base_length_mm": 100.0,
        "base_thickness_mm": 5.0,
        "fin_height_mm": 35.0,
        "fin_length_mm": 100.0,
        "fin_thickness_mm": 1.0,
        "number_of_fins": 26,
        "thermal_result": "Fail",
        "max_chip_temperature_C": 91.47,
        "pressure_drop_Pa": 12.7,
    },
    {
        "case": "CFD-2 reduced-height ducted",
        "description": "80 x 100 x 35 mm ducted heatsink",
        "base_width_mm": 80.0,
        "base_length_mm": 100.0,
        "base_thickness_mm": 5.0,
        "fin_height_mm": 35.0,
        "fin_length_mm": 100.0,
        "fin_thickness_mm": 1.0,
        "number_of_fins": 26,
        "thermal_result": "Slight fail",
        "max_chip_temperature_C": 87.78,
        "pressure_drop_Pa": 44.54,
    },
    {
        "case": "CFD-3 final ducted candidate",
        "description": "80 x 120 x 35 mm ducted heatsink",
        "base_width_mm": 80.0,
        "base_length_mm": 120.0,
        "base_thickness_mm": 5.0,
        "fin_height_mm": 35.0,
        "fin_length_mm": 120.0,
        "fin_thickness_mm": 1.0,
        "number_of_fins": 26,
        "thermal_result": "Pass",
        "max_chip_temperature_C": 83.52,
        "pressure_drop_Pa": 49.02,
    },
]


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def classify_support_risk(mass_g: float) -> str:
    """Classify support risk based on concept-level mass thresholds."""
    if mass_g < LOW_SUPPORT_RISK_MASS_G:
        return "Low"
    elif mass_g < MEDIUM_SUPPORT_RISK_MASS_G:
        return "Medium"
    return "High"


def support_recommendation(risk: str) -> str:
    """Return a concept-level support recommendation."""
    if risk == "Low":
        return "Standard mounting likely acceptable at concept level"
    if risk == "Medium":
        return "Backplate or local stiffening recommended"
    return "Backplate, bracket, standoffs, or chassis/duct support recommended"


def calculate_heatsink_properties(case: dict) -> dict:
    """Calculate volume, mass, weight, and approximate bending moment."""

    base_volume_mm3 = (
        case["base_width_mm"]
        * case["base_length_mm"]
        * case["base_thickness_mm"]
    )

    fin_volume_mm3 = (
        case["number_of_fins"]
        * case["fin_thickness_mm"]
        * case["fin_length_mm"]
        * case["fin_height_mm"]
    )

    total_volume_mm3 = base_volume_mm3 + fin_volume_mm3
    total_volume_cm3 = total_volume_mm3 / 1000.0

    mass_kg = total_volume_mm3 * 1.0e-9 * ALUMINIUM_DENSITY_KG_M3
    mass_g = mass_kg * 1000.0

    weight_N = mass_kg * GRAVITY_M_S2
    bending_moment_Nm = weight_N * (LEVER_ARM_MM / 1000.0)

    support_risk = classify_support_risk(mass_g)

    return {
        **case,
        "base_volume_cm3": base_volume_mm3 / 1000.0,
        "fin_volume_cm3": fin_volume_mm3 / 1000.0,
        "total_volume_cm3": total_volume_cm3,
        "mass_g": mass_g,
        "mass_kg": mass_kg,
        "weight_N": weight_N,
        "lever_arm_mm": LEVER_ARM_MM,
        "approx_bending_moment_Nm": bending_moment_Nm,
        "support_risk": support_risk,
        "support_recommendation": support_recommendation(support_risk),
    }


# ============================================================
# 5. RUN CALCULATIONS
# ============================================================

rows = [calculate_heatsink_properties(case) for case in cases]
df = pd.DataFrame(rows)

output_csv = RESULTS_DIR / "mechanical_support_check.csv"
df.to_csv(output_csv, index=False)


# ============================================================
# 6. CREATE SIMPLE FIGURE
# ============================================================

plt.figure(figsize=(8, 5))
plt.bar(df["case"], df["mass_g"])
plt.axhline(LOW_SUPPORT_RISK_MASS_G, linestyle="--", linewidth=1, label="Low/medium threshold")
plt.axhline(MEDIUM_SUPPORT_RISK_MASS_G, linestyle="--", linewidth=1, label="Medium/high threshold")
plt.ylabel("Estimated heatsink mass (g)")
plt.xlabel("CFD case")
plt.title("Concept-Level Heatsink Mass and Support-Risk Screening")
plt.xticks(rotation=25, ha="right")
plt.legend()
plt.tight_layout()

output_fig = FIGURES_DIR / "heatsink_mass_and_support_risk.png"
plt.savefig(output_fig, dpi=200)
plt.close()


# ============================================================
# 7. PRINT SUMMARY
# ============================================================

print("=" * 80)
print("MECHANICAL SUPPORT CHECK - CONCEPT LEVEL")
print("=" * 80)

display_columns = [
    "case",
    "description",
    "total_volume_cm3",
    "mass_g",
    "weight_N",
    "approx_bending_moment_Nm",
    "support_risk",
    "support_recommendation",
]

print(df[display_columns].to_string(index=False))

print("\nSaved results:")
print(f"- {output_csv}")
print(f"- {output_fig}")

print("\nFinal CFD-3 candidate summary:")
final_case = df[df["case"] == "CFD-3 final ducted candidate"].iloc[0]
print(f"- Estimated mass: {final_case['mass_g']:.2f} g")
print(f"- Weight force: {final_case['weight_N']:.2f} N")
print(f"- Approximate bending moment: {final_case['approx_bending_moment_Nm']:.3f} N.m")
print(f"- Support risk: {final_case['support_risk']}")
print(f"- Recommendation: {final_case['support_recommendation']}")

print("\nImportant limitation:")
print("This is a concept-level mechanical screening only.")
print("It is not a detailed PCB structural FEA, PCIe compliance check, or shock/vibration validation.")