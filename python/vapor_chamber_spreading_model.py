"""
Vapor-chamber / spreading-resistance screening model
====================================================

Purpose
-------
Add chip-to-base spreading resistance to the existing forced-air heatsink model.

Previous forced-air model mainly estimated:
    chip -> TIM -> fin-stack air-side resistance -> air

This script adds:
    chip -> TIM -> base 1D conduction + spreading resistance -> fin-stack -> air

The spreading model uses an equivalent circular source/base approximation for
architecture-level screening.

Important:
- This is not a detailed vapor-chamber two-phase model.
- Vapor chamber is represented as an equivalent anisotropic heat spreader.
- Final CFD/FEA should resolve the real rectangular geometry.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd


# =============================================================================
# Optional SciPy dependency for Bessel functions
# =============================================================================

try:
    from scipy.special import j0, j1, jn_zeros
except ImportError as exc:
    raise ImportError(
        "\nThis script needs scipy for Bessel functions.\n"
        "Install it using:\n\n"
        "    pip install scipy\n\n"
        "Then run the script again.\n"
    ) from exc


# =============================================================================
# Global constants
# =============================================================================

Q_CHIP = 250.0          # W
T_AIR_IN = 25.0        # degC
T_TARGET = 85.0        # degC

# Chip / TIM
CHIP_W = 45e-3         # m
CHIP_L = 45e-3         # m
A_SOURCE = CHIP_W * CHIP_L

TIM_THICKNESS = 0.2e-3     # m
TIM_K_BASELINE = 6.0       # W/mK

# Base thickness used in earlier heatsink concept
BASE_THICKNESS = 5e-3      # m

# Number of Bessel-series terms
N_TERMS = 40


# =============================================================================
# Basic resistance functions
# =============================================================================

def tim_resistance(t_tim: float, k_tim: float, area: float) -> float:
    """
    Bulk TIM resistance only.
    Does not include contact resistance on either side of TIM.
    """
    return t_tim / (k_tim * area)


def equivalent_radius(area: float) -> float:
    """
    Equal-area circular radius.
    A_rect = pi r^2
    """
    return math.sqrt(area / math.pi)


def base_1d_resistance(t_base: float, k_z: float, base_area: float) -> float:
    """
    One-dimensional through-thickness base conduction resistance.

    For isotropic materials: k_z = k.
    For vapor chamber equivalent model: k_z is the effective through-thickness
    conductivity of the assembled spreader.
    """
    return t_base / (k_z * base_area)


# =============================================================================
# Lee/Song/Au/Moran-style equivalent circular spreading model
# =============================================================================

def spreading_resistance_equiv_circular(
    source_area: float,
    base_area: float,
    t_base: float,
    k_model: float,
    h_eff: float,
    n_terms: int = 40,
) -> dict:
    """
    Equivalent circular spreading-resistance estimate.

    Geometry:
        source area -> equivalent radius a
        base area   -> equivalent radius b

    Non-dimensional groups:
        epsilon = a / b
        tau     = t / b
        Bi      = h_eff b / k

    The implemented series follows the common electronics-cooling style
    equivalent circular spreading formulation.

    This returns the excess spreading resistance. The 1D base resistance is
    calculated separately.
    """

    a = equivalent_radius(source_area)
    b = equivalent_radius(base_area)

    epsilon = a / b
    tau = t_base / b
    bi = h_eff * b / k_model

    if epsilon >= 0.999:
        return {
            "R_spreading": 0.0,
            "a_eq_m": a,
            "b_eq_m": b,
            "epsilon": epsilon,
            "tau": tau,
            "Bi": bi,
            "phi": 0.0,
        }

    roots = jn_zeros(1, n_terms)

    summation = 0.0

    for lam in roots:
        numerator = j1(lam * epsilon) ** 2
        denominator = (lam ** 3) * (j0(lam) ** 2)

        # Finite-thickness / convective-boundary correction
        if bi <= 0:
            raise ValueError("Biot number must be positive.")

        bracket = (
            math.tanh(lam * tau) + (lam / bi)
        ) / (
            1.0 + (lam / bi) * math.tanh(lam * tau)
        )

        summation += (numerator / denominator) * bracket

    phi = 2.0 * summation

    r_sp = phi / (2.0 * math.pi * k_model * a)

    return {
        "R_spreading": r_sp,
        "a_eq_m": a,
        "b_eq_m": b,
        "epsilon": epsilon,
        "tau": tau,
        "Bi": bi,
        "phi": phi,
    }


def anisotropic_to_equivalent_isotropic(
    t_physical: float,
    k_xy: float,
    k_z: float,
) -> tuple[float, float]:
    """
    Simple orthotropic-to-equivalent isotropic transformation.

    Vapor chamber is represented as:
        kx = ky = k_xy
        kz = k_z

    Effective transformed thickness:
        t_star = t * sqrt(k_xy / k_z)

    Effective conductivity used in the isotropic spreading equation:
        k_model = sqrt(k_xy * k_z)

    This is an architecture-level approximation, not a detailed two-phase model.
    """

    t_star = t_physical * math.sqrt(k_xy / k_z)
    k_model = math.sqrt(k_xy * k_z)

    return t_star, k_model


# =============================================================================
# Air-side forced-convection cases
# =============================================================================

def load_air_side_cases() -> pd.DataFrame:
    """
    Load useful forced-air cases from previous CSVs if available.
    If not available, use manually defined cases from earlier analytical results.

    The previous forced-air model did not include spreading resistance.
    Therefore, R_air is reconstructed from:
        Tchip_previous = Tin + Q * (R_TIM + R_air)
    """

    r_tim_baseline = tim_resistance(TIM_THICKNESS, TIM_K_BASELINE, A_SOURCE)

    cases = []

    robust_csv = Path("results/heatsink_design_sweep_robust_pass_both.csv")

    if robust_csv.exists():
        df = pd.read_csv(robust_csv)

        # Try to select meaningful geometries if present.
        # Required columns from previous sweep:
        # Vch, CFM, Hf, gap, L, fins, Tchip_T, Tchip_ref
        required = {"Vch", "CFM", "Hf", "gap", "L", "Tchip_T", "Tchip_ref"}

        if required.issubset(df.columns):
            # Candidate 1: recommended forced-air candidate
            # V=5 m/s, Hf=50 mm, gap=2 mm, L=100 mm
            selected = df[
                (df["Vch"].round(3) == 5.0)
                & (df["Hf"].round(3) == 50)
                & (df["gap"].round(3) == 2)
                & (df["L"].round(3) == 100)
            ]

            if not selected.empty:
                row = selected.iloc[0]
                r_air = (row["Tchip_T"] - T_AIR_IN) / Q_CHIP - r_tim_baseline

                cases.append(
                    {
                        "case_name": "Recommended forced-air candidate 80x100x50mm",
                        "base_width_m": 80e-3,
                        "base_length_m": 100e-3,
                        "fin_height_mm": row["Hf"],
                        "length_mm": row["L"],
                        "gap_mm": row["gap"],
                        "velocity_m_s": row["Vch"],
                        "cfm": row["CFM"],
                        "R_air_K_W": r_air,
                        "source": "from robust sweep CSV, reconstructed from Tchip_T",
                    }
                )

            # Candidate 2: compact-ish robust case if exists
            selected2 = df[
                (df["Hf"].round(3) == 40)
                & (df["gap"].round(3) == 2)
                & (df["L"].round(3) == 100)
            ]

            if not selected2.empty:
                row = selected2.sort_values("Vch").iloc[0]
                r_air = (row["Tchip_T"] - T_AIR_IN) / Q_CHIP - r_tim_baseline

                cases.append(
                    {
                        "case_name": "Moderate forced-air candidate 80x100x40mm",
                        "base_width_m": 80e-3,
                        "base_length_m": 100e-3,
                        "fin_height_mm": row["Hf"],
                        "length_mm": row["L"],
                        "gap_mm": row["gap"],
                        "velocity_m_s": row["Vch"],
                        "cfm": row["CFM"],
                        "R_air_K_W": r_air,
                        "source": "from robust sweep CSV, reconstructed from Tchip_T",
                    }
                )

    # Fallback/manual cases based on previously printed analytical results.
    # Baseline 80x80x25 at 4 m/s:
    # Previous Teertstra Tchip ≈ 128.5 C including TIM, so:
    # R_air = (128.5 - 25)/250 - R_TIM
    if not any("Compact baseline" in c["case_name"] for c in cases):
        r_air_baseline = (128.5 - T_AIR_IN) / Q_CHIP - r_tim_baseline

        cases.append(
            {
                "case_name": "Compact baseline 80x80x25mm at 4 m/s",
                "base_width_m": 80e-3,
                "base_length_m": 80e-3,
                "fin_height_mm": 25,
                "length_mm": 80,
                "gap_mm": 2,
                "velocity_m_s": 4.0,
                "cfm": 10.6,
                "R_air_K_W": r_air_baseline,
                "source": "manual fallback from previous baseline result",
            }
        )

    # Fallback recommended candidate:
    # Previous Teertstra Tchip ≈ 79.7 C including TIM, so:
    # R_air = (79.7 - 25)/250 - R_TIM
    if not any("Recommended forced-air" in c["case_name"] for c in cases):
        r_air_recommended = (79.7 - T_AIR_IN) / Q_CHIP - r_tim_baseline

        cases.append(
            {
                "case_name": "Recommended forced-air candidate 80x100x50mm",
                "base_width_m": 80e-3,
                "base_length_m": 100e-3,
                "fin_height_mm": 50,
                "length_mm": 100,
                "gap_mm": 2,
                "velocity_m_s": 5.0,
                "cfm": 26.5,
                "R_air_K_W": r_air_recommended,
                "source": "manual fallback from previous recommended result",
            }
        )

    return pd.DataFrame(cases)


# =============================================================================
# Base / spreader architecture cases
# =============================================================================

def architecture_cases() -> list[dict]:
    """
    Define solid and vapor-chamber-equivalent spreading cases.

    Notes:
    - Al and Cu are isotropic.
    - VC cases are equivalent anisotropic sensitivity cases.
    - VC values are not claimed as exact product data.
    """

    return [
        {
            "architecture": "Aluminum 6061 base",
            "type": "isotropic",
            "k_iso_W_mK": 167.0,
            "k_xy_W_mK": 167.0,
            "k_z_W_mK": 167.0,
            "note": "isotropic solid aluminum, conservative alloy",
        },
        {
            "architecture": "Aluminum high-k base",
            "type": "isotropic",
            "k_iso_W_mK": 200.0,
            "k_xy_W_mK": 200.0,
            "k_z_W_mK": 200.0,
            "note": "isotropic aluminum screening value",
        },
        {
            "architecture": "Copper spreader",
            "type": "isotropic",
            "k_iso_W_mK": 385.0,
            "k_xy_W_mK": 385.0,
            "k_z_W_mK": 385.0,
            "note": "isotropic copper spreader",
        },
        {
            "architecture": "Vapor chamber conservative",
            "type": "anisotropic",
            "k_iso_W_mK": None,
            "k_xy_W_mK": 2000.0,
            "k_z_W_mK": 150.0,
            "note": "equivalent VC spreader, conservative through-thickness behavior",
        },
        {
            "architecture": "Vapor chamber baseline",
            "type": "anisotropic",
            "k_iso_W_mK": None,
            "k_xy_W_mK": 2500.0,
            "k_z_W_mK": 300.0,
            "note": "equivalent VC spreader, moderate literature-style in-plane value",
        },
        {
            "architecture": "Vapor chamber optimistic sensitivity",
            "type": "anisotropic",
            "k_iso_W_mK": None,
            "k_xy_W_mK": 10000.0,
            "k_z_W_mK": 400.0,
            "note": "optimistic sensitivity only, not claimed as exact product data",
        },
    ]


# =============================================================================
# Main analysis
# =============================================================================

def run_analysis() -> pd.DataFrame:
    r_tim = tim_resistance(TIM_THICKNESS, TIM_K_BASELINE, A_SOURCE)

    air_cases = load_air_side_cases()
    arch_cases = architecture_cases()

    rows = []

    for _, air in air_cases.iterrows():
        base_area = air["base_width_m"] * air["base_length_m"]
        r_air = air["R_air_K_W"]

        # Effective uniform heat-transfer coefficient from air-side resistance.
        # Use full base area, not chip area.
        h_eff = 1.0 / (r_air * base_area)

        for arch in arch_cases:
            if arch["type"] == "isotropic":
                k_z = arch["k_z_W_mK"]
                k_model = arch["k_iso_W_mK"]
                t_model = BASE_THICKNESS
            else:
                k_xy = arch["k_xy_W_mK"]
                k_z = arch["k_z_W_mK"]

                t_model, k_model = anisotropic_to_equivalent_isotropic(
                    t_physical=BASE_THICKNESS,
                    k_xy=k_xy,
                    k_z=k_z,
                )

            r_1d = base_1d_resistance(
                t_base=BASE_THICKNESS,
                k_z=k_z,
                base_area=base_area,
            )

            sp = spreading_resistance_equiv_circular(
                source_area=A_SOURCE,
                base_area=base_area,
                t_base=t_model,
                k_model=k_model,
                h_eff=h_eff,
                n_terms=N_TERMS,
            )

            r_sp = sp["R_spreading"]

            r_solid = r_tim + r_1d + r_sp
            r_total = r_solid + r_air

            t_chip = T_AIR_IN + Q_CHIP * r_total
            margin = T_TARGET - t_chip

            rows.append(
                {
                    "air_case": air["case_name"],
                    "air_case_source": air["source"],
                    "base_width_mm": air["base_width_m"] * 1e3,
                    "base_length_mm": air["base_length_m"] * 1e3,
                    "base_area_mm2": base_area * 1e6,
                    "velocity_m_s": air["velocity_m_s"],
                    "cfm": air["cfm"],
                    "architecture": arch["architecture"],
                    "architecture_type": arch["type"],
                    "k_xy_W_mK": arch["k_xy_W_mK"],
                    "k_z_W_mK": arch["k_z_W_mK"],
                    "k_model_W_mK": k_model,
                    "t_physical_mm": BASE_THICKNESS * 1e3,
                    "t_model_mm": t_model * 1e3,
                    "h_eff_W_m2K": h_eff,
                    "a_eq_mm": sp["a_eq_m"] * 1e3,
                    "b_eq_mm": sp["b_eq_m"] * 1e3,
                    "epsilon": sp["epsilon"],
                    "tau": sp["tau"],
                    "Bi": sp["Bi"],
                    "phi": sp["phi"],
                    "R_TIM_K_W": r_tim,
                    "R_base_1D_K_W": r_1d,
                    "R_spreading_K_W": r_sp,
                    "R_solid_K_W": r_solid,
                    "R_air_K_W": r_air,
                    "R_total_K_W": r_total,
                    "T_chip_C": t_chip,
                    "thermal_margin_C": margin,
                    "status": "PASS" if t_chip <= T_TARGET else "FAIL",
                    "note": arch["note"],
                }
            )

    return pd.DataFrame(rows)


def print_summary(df: pd.DataFrame) -> None:
    print("\nVapor-chamber / spreading-resistance screening")
    print("=" * 110)
    print(f"Chip power                 : {Q_CHIP:.1f} W")
    print(f"Inlet air temperature       : {T_AIR_IN:.1f} degC")
    print(f"Target chip temperature     : {T_TARGET:.1f} degC")
    print(f"Chip/source area            : {A_SOURCE * 1e6:.1f} mm^2")
    print(f"TIM resistance              : {df['R_TIM_K_W'].iloc[0]:.5f} K/W")
    print("-" * 110)

    columns = [
        "air_case",
        "architecture",
        "R_TIM_K_W",
        "R_base_1D_K_W",
        "R_spreading_K_W",
        "R_air_K_W",
        "R_total_K_W",
        "T_chip_C",
        "thermal_margin_C",
        "status",
    ]

    compact = df[columns].copy()

    compact["R_TIM_K_W"] = compact["R_TIM_K_W"].map(lambda x: f"{x:.4f}")
    compact["R_base_1D_K_W"] = compact["R_base_1D_K_W"].map(lambda x: f"{x:.4f}")
    compact["R_spreading_K_W"] = compact["R_spreading_K_W"].map(lambda x: f"{x:.4f}")
    compact["R_air_K_W"] = compact["R_air_K_W"].map(lambda x: f"{x:.4f}")
    compact["R_total_K_W"] = compact["R_total_K_W"].map(lambda x: f"{x:.4f}")
    compact["T_chip_C"] = compact["T_chip_C"].map(lambda x: f"{x:.1f}")
    compact["thermal_margin_C"] = compact["thermal_margin_C"].map(lambda x: f"{x:.1f}")

    with pd.option_context("display.max_rows", None, "display.max_columns", None, "display.width", 220):
        print(compact.to_string(index=False))

    print("-" * 110)

    # Show best architecture per air case
    print("\nBest architecture per air-side case:")
    print("-" * 110)

    best_rows = (
        df.sort_values(["air_case", "T_chip_C"])
        .groupby("air_case", as_index=False)
        .first()
    )

    for _, row in best_rows.iterrows():
        print(
            f"{row['air_case']}\n"
            f"  Best architecture : {row['architecture']}\n"
            f"  T_chip            : {row['T_chip_C']:.1f} degC\n"
            f"  Margin            : {row['thermal_margin_C']:.1f} degC\n"
            f"  R_air             : {row['R_air_K_W']:.4f} K/W\n"
            f"  R_spreading       : {row['R_spreading_K_W']:.4f} K/W\n"
            f"  Interpretation    : "
            f"{'air-side dominated' if row['R_air_K_W'] > 3 * row['R_spreading_K_W'] else 'solid/spreading resistance important'}\n"
        )


def main() -> None:
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    df = run_analysis()

    output_file = results_dir / "vapor_chamber_spreading_model.csv"
    df.to_csv(output_file, index=False)

    print_summary(df)

    print(f"\nFull CSV saved to: {output_file}")


if __name__ == "__main__":
    main()