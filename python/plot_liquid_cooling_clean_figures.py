# plot_liquid_cooling_clean_figures.py
# Creates presentation-quality figures from the liquid cooling screening CSV files.
#
# This script does not change the physics or calculations.
# It only improves figure presentation and produces:
# - figures/liquid_flow_required.png
# - figures/liquid_convective_screening.png
# - figures/immersion_architecture_progression.png
# - figures/cold_plate_flow_sensitivity.png

from pathlib import Path
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
# 2. STYLE HELPERS
# ============================================================

def apply_common_style(ax):
    ax.grid(True, which="both", axis="y", alpha=0.25)
    ax.grid(True, which="major", axis="x", alpha=0.12)
    ax.tick_params(axis="both", labelsize=11)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)


def apply_log_y_plain_ticks(ax):
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(formatter)


def apply_log_x_plain_ticks(ax):
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    ax.xaxis.set_major_formatter(formatter)


def annotate_vertical_bars(ax, bars, values, unit, log_scale=True):
    for bar, value in zip(bars, values):
        x = bar.get_x() + bar.get_width() / 2
        y = value * 1.08 if log_scale else value + 0.03 * max(values)
        if value >= 100:
            label = f"{value:.0f} {unit}"
        elif value >= 10:
            label = f"{value:.1f} {unit}"
        else:
            label = f"{value:.2f} {unit}"
        ax.text(x, y, label, ha="center", va="bottom", fontsize=9)


def short_fluid_name(name):
    mapping = {
        "Air": "Air",
        "Water-like coolant": "Water-like liquid",
        "Representative dielectric liquid": "Dielectric liquid",
    }
    return mapping.get(name, name)


def case_plot_name(name):
    mapping = {
        "Direct-to-chip cold plate": "Cold plate\n(minichannel)",
        "Bare immersion flat plate": "Immersion\nbare 45 × 45 mm",
        "Spreader-only immersion flat plate": "Immersion\nspread 80 × 80 mm",
        "Finned immersion heat spreader": "Immersion\nfinned spreader",
    }
    return mapping.get(name, name)


# ============================================================
# 3. LOAD DATA
# ============================================================

flow_df = pd.read_csv(FLOW_FILE)
h_df = pd.read_csv(H_FILE)

flow_df["fluid_plot"] = flow_df["fluid"].apply(short_fluid_name)
h_df["case_plot"] = h_df["case"].apply(case_plot_name)

# Component-level rows only
component_df = h_df[h_df["case"] != "Air cooling CFD-3 reference"].copy()

case_order = [
    "Direct-to-chip cold plate",
    "Bare immersion flat plate",
    "Spreader-only immersion flat plate",
    "Finned immersion heat spreader",
]

component_df["plot_order"] = component_df["case"].apply(
    lambda x: case_order.index(x) if x in case_order else 999
)
component_df = component_df.sort_values("plot_order")


# ============================================================
# 4. FIGURE 1:
# FLOW REQUIRED FOR 5 K, 10 K, AND 15 K BULK RISE
# ============================================================

flow_pivot = flow_df.pivot_table(
    index="coolant_delta_T_K",
    columns="fluid_plot",
    values="volume_flow_L_min",
    aggfunc="first",
)

# Order columns deliberately
flow_columns = ["Air", "Water-like liquid", "Dielectric liquid"]
flow_pivot = flow_pivot[flow_columns]

x_labels = [f"{int(x)} K" for x in flow_pivot.index]
x = list(range(len(x_labels)))
bar_width = 0.23

fig, ax = plt.subplots(figsize=(11, 6.2))

for i, col in enumerate(flow_columns):
    offsets = [xi + (i - 1) * bar_width for xi in x]
    bars = ax.bar(offsets, flow_pivot[col].values, width=bar_width, label=col)
    annotate_vertical_bars(
        ax,
        bars,
        flow_pivot[col].values,
        "L/min",
        log_scale=True,
    )

ax.set_yscale("log")
ax.set_xticks(x)
ax.set_xticklabels(x_labels)
ax.set_xlabel("Allowed bulk coolant temperature rise, ΔT", fontsize=12)
ax.set_ylabel("Required volume flow rate [L/min, log scale]", fontsize=12)
ax.set_title(
    "Coolant flow required to carry 250 W\nQ = m_dot cp ΔT",
    fontsize=16,
)
ax.legend(frameon=False, fontsize=11)
apply_common_style(ax)
apply_log_y_plain_ticks(ax)

fig.tight_layout()
fig.savefig(FIGURES_DIR / "liquid_flow_required.png", dpi=300)
plt.close(fig)


# ============================================================
# 5. FIGURE 2:
# CONVECTIVE SCREENING, h AND SURFACE-TO-FLUID DELTA T
# ============================================================

x_labels = component_df["case_plot"].tolist()
x = list(range(len(x_labels)))

h_values = component_df["h_W_m2K"].values
dt_values = component_df["surface_to_fluid_delta_T_K"].values

fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))

# Left: heat-transfer coefficient h
ax = axes[0]
bars_h = ax.bar(x, h_values)
ax.set_yscale("log")
ax.set_xticks(x)
ax.set_xticklabels(x_labels)
ax.set_ylabel("Convective heat-transfer coefficient, h [W/m²K, log scale]", fontsize=12)
ax.set_title("Heat-transfer coefficient\ncomponent-level screening", fontsize=15)

annotate_vertical_bars(ax, bars_h, h_values, "W/m²K", log_scale=True)

apply_common_style(ax)
apply_log_y_plain_ticks(ax)

# Right: surface-to-fluid delta T
ax = axes[1]
bars_dt = ax.bar(x, dt_values)
ax.set_yscale("log")
ax.set_xticks(x)
ax.set_xticklabels(x_labels)
ax.set_ylabel("Surface-to-fluid temperature rise, ΔT [K, log scale]", fontsize=12)
ax.set_title("Surface-to-fluid temperature rise\ncomponent-level screening", fontsize=15)

annotate_vertical_bars(ax, bars_dt, dt_values, "K", log_scale=True)

ax.axhline(
    CFD3_CHIP_RISE_K,
    linestyle="--",
    linewidth=1.8,
    color="black",
    alpha=0.7,
)

ax.text(
    1.65,
    CFD3_CHIP_RISE_K * 1.16,
    "CFD-3 air-cooled chip rise = 58.52 K\n"
    "system-level reference only",
    ha="center",
    va="bottom",
    fontsize=9,
    style="italic",
)

apply_common_style(ax)
apply_log_y_plain_ticks(ax)

fig.suptitle(
    "Liquid and immersion cooling screening: h, area, and architecture effects",
    fontsize=17,
    y=1.02,
)

fig.tight_layout()
fig.savefig(FIGURES_DIR / "liquid_convective_screening.png", dpi=300, bbox_inches="tight")
plt.close(fig)


# ============================================================
# 6. FIGURE 3:
# IMMERSION ARCHITECTURE PROGRESSION
# ============================================================

immersion_cases = [
    "Bare immersion flat plate",
    "Spreader-only immersion flat plate",
    "Finned immersion heat spreader",
]

immersion_df = h_df[h_df["case"].isin(immersion_cases)].copy()
immersion_df["plot_order"] = immersion_df["case"].apply(immersion_cases.index)
immersion_df = immersion_df.sort_values("plot_order")

x_labels = [
    "Bare chip immersion\n45 × 45 mm",
    "Flat spreader\n80 × 80 mm",
    "Finned spreader\n80 × 80 mm",
]

dt_values = immersion_df["surface_to_fluid_delta_T_K"].values

fig, ax = plt.subplots(figsize=(10, 5.8))

ax.plot(
    range(len(x_labels)),
    dt_values,
    marker="o",
    linewidth=2.5,
)

ax.set_yscale("log")
ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels)
ax.set_ylabel("Surface-to-fluid temperature rise, ΔT [K, log scale]", fontsize=12)
ax.set_title("Immersion architecture progression", fontsize=16)

for i, value in enumerate(dt_values):
    ax.text(
        i,
        value * 1.10,
        f"{value:.1f} K",
        ha="center",
        va="bottom",
        fontsize=10,
    )

ax.axhline(
    CFD3_CHIP_RISE_K,
    linestyle="--",
    linewidth=1.8,
    color="black",
    alpha=0.7,
)

ax.text(
    1,
    CFD3_CHIP_RISE_K * 1.15,
    "CFD-3 air-cooled chip-rise reference = 58.52 K\n"
    "not directly comparable to component-level bars",
    ha="center",
    va="bottom",
    fontsize=9,
    style="italic",
)

apply_common_style(ax)
apply_log_y_plain_ticks(ax)

fig.tight_layout()
fig.savefig(FIGURES_DIR / "immersion_architecture_progression.png", dpi=300)
plt.close(fig)


# ============================================================
# 7. FIGURE 4:
# COLD-PLATE FLOW SENSITIVITY
# ============================================================

if COLD_PLATE_FILE.exists():
    cp_df = pd.read_csv(COLD_PLATE_FILE)

    fig, ax = plt.subplots(figsize=(10, 5.8))

    ax.plot(
        cp_df["water_volume_flow_L_min"],
        cp_df["surface_to_fluid_delta_T_K"],
        marker="o",
        linewidth=2.3,
    )

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlabel("Water-like coolant flow rate [L/min, log scale]", fontsize=12)
    ax.set_ylabel("Surface-to-fluid temperature rise, ΔT [K, log scale]", fontsize=12)
    ax.set_title("Cold-plate flow sensitivity under simplified Nu model", fontsize=16)

    for _, row in cp_df.iterrows():
        ax.text(
            row["water_volume_flow_L_min"] * 1.05,
            row["surface_to_fluid_delta_T_K"] * 1.05,
            f"{row['surface_to_fluid_delta_T_K']:.1f} K",
            fontsize=9,
        )

    ax.text(
        0.03,
        0.06,
        "Laminar branch uses constant Nu = 4.12.\n"
        "Developing-flow effects and pressure drop are not included.",
        transform=ax.transAxes,
        fontsize=9,
        va="bottom",
        bbox=dict(facecolor="white", alpha=0.75, edgecolor="none"),
    )

    ax.grid(True, which="both", alpha=0.25)
    ax.tick_params(axis="both", labelsize=11)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    apply_log_x_plain_ticks(ax)
    apply_log_y_plain_ticks(ax)

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "cold_plate_flow_sensitivity.png", dpi=300)
    plt.close(fig)


# ============================================================
# 8. PRINT OUTPUT
# ============================================================

print("Updated liquid-cooling figures generated successfully.")
print()
print("Saved files:")
print(f"- {FIGURES_DIR / 'liquid_flow_required.png'}")
print(f"- {FIGURES_DIR / 'liquid_convective_screening.png'}")
print(f"- {FIGURES_DIR / 'immersion_architecture_progression.png'}")
if COLD_PLATE_FILE.exists():
    print(f"- {FIGURES_DIR / 'cold_plate_flow_sensitivity.png'}")
else:
    print("- cold_plate_flow_sensitivity.png skipped because CSV was not found.")
