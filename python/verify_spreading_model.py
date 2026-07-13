"""
Verification checks for spreading-resistance model
==================================================

Purpose
-------
This script checks whether the spreading-resistance subfunction used in
vapor_chamber_spreading_model.py behaves physically.

Checks:
1. No-spreading limit:
   If source area = base area, R_spreading should be zero.

2. Area-ratio trend:
   If the base area becomes larger than the source area, R_spreading should increase.

3. Material trend:
   Copper should give lower spreading resistance than aluminum.

This verification is important before using the model results in the report.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

# Import the actual spreading function from the main model file
from vapor_chamber_spreading_model import spreading_resistance_equiv_circular


# -------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------

SOURCE_SIDE = 45e-3          # m
A_SOURCE = SOURCE_SIDE * SOURCE_SIDE

BASE_THICKNESS = 5e-3        # m

# Representative effective heat-transfer coefficient.
# This value is not the main subject of the verification.
# It only provides a positive convective boundary condition.
H_EFF = 600.0                # W/m2K

K_AL = 167.0                 # W/mK
K_CU = 385.0                 # W/mK


def run_verification() -> pd.DataFrame:
    rows = []

    base_cases = [
        {
            "case": "No spreading: 45x45 source to 45x45 base",
            "base_w_m": 45e-3,
            "base_l_m": 45e-3,
        },
        {
            "case": "Mild spreading: 45x45 source to 60x60 base",
            "base_w_m": 60e-3,
            "base_l_m": 60e-3,
        },
        {
            "case": "Project compact base: 45x45 source to 80x80 base",
            "base_w_m": 80e-3,
            "base_l_m": 80e-3,
        },
        {
            "case": "Project recommended base: 45x45 source to 80x100 base",
            "base_w_m": 80e-3,
            "base_l_m": 100e-3,
        },
        {
            "case": "Large spreading: 45x45 source to 120x120 base",
            "base_w_m": 120e-3,
            "base_l_m": 120e-3,
        },
    ]

    materials = [
        {"material": "Aluminum 6061", "k_W_mK": K_AL},
        {"material": "Copper", "k_W_mK": K_CU},
    ]

    for base in base_cases:
        base_area = base["base_w_m"] * base["base_l_m"]
        area_ratio = base_area / A_SOURCE

        for mat in materials:
            result = spreading_resistance_equiv_circular(
                source_area=A_SOURCE,
                base_area=base_area,
                t_base=BASE_THICKNESS,
                k_model=mat["k_W_mK"],
                h_eff=H_EFF,
                n_terms=40,
            )

            rows.append(
                {
                    "case": base["case"],
                    "material": mat["material"],
                    "base_width_mm": base["base_w_m"] * 1e3,
                    "base_length_mm": base["base_l_m"] * 1e3,
                    "area_ratio_Abase_Asource": area_ratio,
                    "k_W_mK": mat["k_W_mK"],
                    "epsilon": result["epsilon"],
                    "tau": result["tau"],
                    "Bi": result["Bi"],
                    "phi": result["phi"],
                    "R_spreading_K_W": result["R_spreading"],
                    "DeltaT_spreading_at_250W_C": 250.0 * result["R_spreading"],
                }
            )

    return pd.DataFrame(rows)


def print_summary(df: pd.DataFrame) -> None:
    print("\nSpreading-model verification")
    print("=" * 100)
    print("Check 1: If source area = base area, R_spreading should be zero.")
    print("Check 2: R_spreading should increase as base area becomes larger than source area.")
    print("Check 3: Copper should have lower R_spreading than aluminum.")
    print("-" * 100)

    compact = df[
        [
            "case",
            "material",
            "area_ratio_Abase_Asource",
            "epsilon",
            "R_spreading_K_W",
            "DeltaT_spreading_at_250W_C",
        ]
    ].copy()

    compact["area_ratio_Abase_Asource"] = compact["area_ratio_Abase_Asource"].map(
        lambda x: f"{x:.2f}"
    )
    compact["epsilon"] = compact["epsilon"].map(lambda x: f"{x:.3f}")
    compact["R_spreading_K_W"] = compact["R_spreading_K_W"].map(lambda x: f"{x:.6f}")
    compact["DeltaT_spreading_at_250W_C"] = compact[
        "DeltaT_spreading_at_250W_C"
    ].map(lambda x: f"{x:.3f}")

    with pd.option_context(
        "display.max_rows", None,
        "display.max_columns", None,
        "display.width", 220,
    ):
        print(compact.to_string(index=False))

    print("-" * 100)

    # Simple pass/fail logic
    no_spreading = df[df["area_ratio_Abase_Asource"].round(6) == 1.0]
    max_no_spreading = no_spreading["R_spreading_K_W"].abs().max()

    if max_no_spreading < 1e-10:
        print("PASS: No-spreading limit gives R_spreading ≈ 0.")
    else:
        print("WARNING: No-spreading limit did not give near-zero spreading resistance.")

    # Trend check for aluminum
    al = df[df["material"] == "Aluminum 6061"].sort_values(
        "area_ratio_Abase_Asource"
    )
    is_increasing = al["R_spreading_K_W"].is_monotonic_increasing

    if is_increasing:
        print("PASS: Aluminum R_spreading increases with base/source area ratio.")
    else:
        print("WARNING: Aluminum R_spreading trend is not monotonic.")

    # Copper lower than aluminum check for each case
    trend_ok = True
    for case_name in df["case"].unique():
        sub = df[df["case"] == case_name]
        r_al = sub[sub["material"] == "Aluminum 6061"]["R_spreading_K_W"].iloc[0]
        r_cu = sub[sub["material"] == "Copper"]["R_spreading_K_W"].iloc[0]
        if r_cu > r_al:
            trend_ok = False

    if trend_ok:
        print("PASS: Copper gives lower R_spreading than aluminum for every case.")
    else:
        print("WARNING: Copper did not always give lower R_spreading.")

    print("=" * 100)


def main() -> None:
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    df = run_verification()

    output_file = results_dir / "verify_spreading_model.csv"
    df.to_csv(output_file, index=False)

    print_summary(df)

    print(f"\nFull CSV saved to: {output_file}")


if __name__ == "__main__":
    main()