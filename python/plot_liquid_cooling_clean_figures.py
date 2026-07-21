# plot_liquid_cooling_clean_figures.py
# Creates cleaner presentation-quality figures from the liquid cooling screening CSV files.
#
# This script does not change the physics or calculations.
# It only improves figure presentation:
# - horizontal bars instead of default vertical bars
# - shorter labels
# - direct value annotations
# - clearer separation between component-level screening and CFD-3 system-level reference
# - cleaner immersion progression plot

from pathlib import Path
import textwrap
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter


# ============================================================
# 1. PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures"

FIGURES_DIR.mkdir(exist_ok=True)

FLOW_FILE = RESULTS_DIR / "flow_rate_comparison.csv"
H_FILE = RESULTS_DIR / "h_screening_summary.csv"
COLD_PLATE_FILE = RESULTS_DIR / "cold_plate_flow_sensitivity.csv"

CFD3_CHIP_RISE_K = 58.52


# ============================================================
# 2. HELPER FUNCTIONS
# ============================================================

def wrap_label(text, width=24):
    """Wrap long labels so axes do not need tilted text."""
    return "\n".join(textwrap.wrap(str(text), width=width))


def short_fluid_name(name):
    mapping = {
        "Air": "Air",
        "Water-like coolant": "Water-like coolant",
        "Representative dielectric liquid": "Dielectric liquid",
    }
    return mapping.get(name, name)


def short_case_name(name):
    mapping = {
        "Air cooling CFD-3 reference": "Air cooling CFD-3 reference",
        "Direct-to-chip cold plate": "Direct-to-chip cold plate",
        "Bare immersion flat plate": "Bare immersion flat plate",
        "Spreader-only immersion flat plate": "Spreader-only immersion flat plate",
        "Finned immersion heat spreader": "Finned immersion heat spreader",
    }
    return mapping.get(name, name)


def annotate_horizontal_bars(ax, values, fmt_func, log_scale=True):
    """Add value labels to horizontal bars."""
    for i, value in enumerate(values):
        x_text = value * 1.08 if log_scale else value * 1.01
        ax.text(
            x_text,
            i,
            fmt_func(value),
            va="center",
            fontsize=10,
        )


def set_plain_log_ticks(ax):
    """Make log-axis tick labels easier to read."""
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    ax.xaxis.set_major_formatter(formatter)


# ============================================================
# 3. LOAD DATA
# ============================================================

flow_df = pd.read_csv(FLOW_FILE)
h_df = pd.read_csv(H_FILE)

flow_df["fluid_short"] = flow_df["fluid"].apply(short_fluid_name)
h_df["case_short"] = h_df["case"].apply(short_case_name)


# ============================================================
# 4. FIGURE 1:
# REQUIRED COOLANT FLOW AT 10 K BULK TEMPERATURE RISE
# ============================================================

flow_10k = flow_df[flow_df["coolant_delta_T_K"] == 10.0].copy()

flow_10k = flow_10k[[
    "fluid_short",
    "volume_flow_L_min",
]].sort_values("volume_flow_L_min", ascending=True)

fig, ax = plt.subplots(figsize=(10, 5.5))

ax.barh(
    flow_10k["fluid_short"],
    flow_10k["volume_flow_L_min"],
)

ax.set_xscale("log")
ax.set_xlabel("Required volume flow rate [L/min, log scale]", fontsize=12)
ax.set_title(
    "Coolant flow required to carry 250 W at 10 K bulk temperature rise",
    fontsize=15,
)
ax.grid(True, axis="x", which="both", alpha=0.30)

annotate_horizontal_bars(
    ax,
    flow_10k["volume_flow_L_min"].values,
    lambda v: f"{v:.3f} L/min" if v < 10 else f"{v:.1f} L/min",
    log_scale=True,
)

set_plain_log_ticks(ax)
ax.tick_params(axis="both", labelsize=11)

fig.tight_layout()
fig.savefig(FIGURES_DIR / "liquid_flow_required_10K_clean.png", dpi=300)
plt.close(fig)


# ============================================================
# 5. FIGURE 2:
# COMPONENT-LEVEL CONVECTIVE SCREENING
# ============================================================
# Air CFD-3 is NOT plotted as a bar because it is a system-level CFD result.
# It is shown only as a dashed reference line.

component_df = h_df[h_df["case_short"] != "Air cooling CFD-3 reference"].copy()

case_order = [
    "Direct-to-chip cold plate",
    "Finned immersion heat spreader",
    "Spreader-only immersion flat plate",
    "Bare immersion flat plate",
]

component_df["plot_order"] = component_df["case_short"].apply(
    lambda x: case_order.index(x) if x in case_order else 999
)

component_df = component_df.sort_values("plot_order")
component_df["case_plot"] = component_df["case_short"].apply(
    lambda x: wrap_label(x, width=26)
)

fig, ax = plt.subplots(figsize=(11, 6.5))

ax.barh(
    component_df["case_plot"],
    component_df["surface_to_fluid_delta_T_K"],
)

ax.set_xscale("log")
ax.set_xlabel(
    "Estimated surface-to-fluid temperature rise [K, log scale]",
    fontsize=12,
)
ax.set_title(
    "Convective screening: effect of cooling architecture and wetted area",
    fontsize=15,
)
ax.grid(True, axis="x", which="both", alpha=0.30)

ax.axvline(
    CFD3_CHIP_RISE_K,
    linestyle="--",
    linewidth=2,
    label=f"CFD-3 air-cooled chip rise above inlet = {CFD3_CHIP_RISE_K:.2f} K",
)

ax.legend(loc="lower right", fontsize=10)

annotate_horizontal_bars(
    ax,
    component_df["surface_to_fluid_delta_T_K"].values,
    lambda v: f"{v:.1f} K",
    log_scale=True,
)

set_plain_log_ticks(ax)
ax.tick_params(axis="both", labelsize=11)

fig.tight_layout()
fig.savefig(FIGURES_DIR / "component_level_convective_screening_clean.png", dpi=300)
plt.close(fig)


# ============================================================
# 6. FIGURE 3:
# IMMERSION ARCHITECTURE PROGRESSION
# ============================================================
# This shows the design logic:
# bare chip immersion -> flat spreader -> finned spreader

immersion_df = h_df[h_df["case_short"].isin([
    "Bare immersion flat plate",
    "Spreader-only immersion flat plate",
    "Finned immersion heat spreader",
])].copy()

immersion_order = [
    "Bare immersion flat plate",
    "Spreader-only immersion flat plate",
    "Finned immersion heat spreader",
]

immersion_df["plot_order"] = immersion_df["case_short"].apply(
    lambda x: immersion_order.index(x)
)

immersion_df = immersion_df.sort_values("plot_order")

x_labels = [
    "Bare immersion\n45 × 45 mm chip",
    "Spreader-only\n80 × 80 mm",
    "Finned spreader\n80 × 80 mm",
]

y_values = immersion_df["surface_to_fluid_delta_T_K"].values

fig, ax = plt.subplots(figsize=(9.5, 5.5))

ax.plot(
    x_labels,
    y_values,
    marker="o",
    linewidth=2,
)

ax.set_yscale("log")
ax.set_ylabel(
    "Estimated surface-to-fluid temperature rise [K, log scale]",
    fontsize=12,
)
ax.set_title(
    "Immersion architecture progression",
    fontsize=15,
)
ax.grid(True, axis="y", which="both", alpha=0.30)

for x, y in zip(x_labels, y_values):
    ax.text(
        x,
        y * 1.08,
        f"{y:.1f} K",
        ha="center",
        fontsize=10,
    )

ax.axhline(
    CFD3_CHIP_RISE_K,
    linestyle="--",
    linewidth=2,
)

ax.text(
    1,
    CFD3_CHIP_RISE_K * 1.10,
    f"CFD-3 air-cooled chip-rise reference = {CFD3_CHIP_RISE_K:.2f} K",
    ha="center",
    fontsize=10,
)

ax.tick_params(axis="both", labelsize=11)

fig.tight_layout()
fig.savefig(FIGURES_DIR / "immersion_architecture_progression_clean.png", dpi=300)
plt.close(fig)


# ============================================================
# 7. FIGURE 4:
# COLD-PLATE FLOW SENSITIVITY
# ============================================================
# This is useful, but should be treated as an appendix/supporting figure.
# The laminar part uses a simplified fully developed constant-Nu model.

if COLD_PLATE_FILE.exists():
    cp_df = pd.read_csv(COLD_PLATE_FILE)

    fig, ax = plt.subplots(figsize=(9.5, 5.5))

    ax.plot(
        cp_df["water_volume_flow_L_min"],
        cp_df["surface_to_fluid_delta_T_K"],
        marker="o",
        linewidth=2,
    )

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlabel(
        "Water-like coolant flow rate [L/min, log scale]",
        fontsize=12,
    )
    ax.set_ylabel(
        "Estimated surface-to-fluid temperature rise [K, log scale]",
        fontsize=12,
    )
    ax.set_title(
        "Cold-plate flow sensitivity under simplified Nu model",
        fontsize=15,
    )

    ax.grid(True, which="both", alpha=0.30)

    for _, row in cp_df.iterrows():
        ax.text(
            row["water_volume_flow_L_min"] * 1.05,
            row["surface_to_fluid_delta_T_K"] * 1.03,
            f"{row['surface_to_fluid_delta_T_K']:.1f} K",
            fontsize=9,
        )

    ax.text(
        0.03,
        0.05,
        "Note: laminar branch uses constant Nu = 4.12;\n"
        "developing-flow effects are not included.",
        transform=ax.transAxes,
        fontsize=9,
        va="bottom",
    )

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "cold_plate_flow_sensitivity_clean.png", dpi=300)
    plt.close(fig)


# ============================================================
# 8. PRINT OUTPUT
# ============================================================

print("Clean figures generated successfully.")
print()
print("Saved files:")
print(f"- {FIGURES_DIR / 'liquid_flow_required_10K_clean.png'}")
print(f"- {FIGURES_DIR / 'component_level_convective_screening_clean.png'}")
print(f"- {FIGURES_DIR / 'immersion_architecture_progression_clean.png'}")

if COLD_PLATE_FILE.exists():
    print(f"- {FIGURES_DIR / 'cold_plate_flow_sensitivity_clean.png'}")
else:
    print("- cold_plate_flow_sensitivity_clean.png skipped because cold_plate_flow_sensitivity.csv was not found.")