# liquid_cooling_screening.py
# Liquid and immersion cooling screening extension for a 250 W PCIe AI accelerator chip.
#
# This script compares:
# 1) coolant heat-carrying capacity using Q = m_dot * cp * DeltaT
# 2) simple convective screening estimates for:
#    - direct-to-chip minichannel cold plate
#    - bare single-phase immersion flat plate
#    - idealized spreader-only immersion flat plate
#    - idealized finned immersion heat-spreader concept
# 3) flow sensitivity for:
#    - cold plate minichannel flow
#    - immersion directed-flow cases
#
# Important:
# This is a first-principles and empirical-correlation screening model only.
# It is NOT a validated liquid-cooling design.
# It is NOT an immersion-tank CFD model.
# It is NOT a chip-junction temperature prediction.
# It is NOT a product qualification model.

from pathlib import Path
import math
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
# 2. GLOBAL DESIGN TARGET
# ============================================================

Q_W = 250.0
T_INLET_AIR_C = 25.0
T_CHIP_TARGET_C = 85.0

CHIP_LENGTH_M = 0.045
CHIP_WIDTH_M = 0.045
CHIP_AREA_M2 = CHIP_LENGTH_M * CHIP_WIDTH_M

DELTA_T_COOLANT_LIST_K = [5.0, 10.0, 15.0]

# Existing air-cooled CFD-3 reference result from this project.
# This is a system-level conjugate heat-transfer CFD result.
# It includes chip/TIM/heatsink/airflow effects and should not be treated
# as identical to the component-level convective estimates below.
AIR_CFD3_T_CHIP_MAX_C = 83.52
AIR_CFD3_CHIP_RISE_ABOVE_INLET_K = AIR_CFD3_T_CHIP_MAX_C - T_INLET_AIR_C
AIR_CFD3_PRESSURE_DROP_PA = 49.02


# ============================================================
# 3. REPRESENTATIVE FLUID PROPERTIES
# ============================================================
# These are representative screening values.
# They are not tied to one commercial coolant product.

fluids = {
    "Air": {
        "cooling_method": "Air-cooled ducted heatsink",
        "rho_kg_m3": 1.20,
        "cp_J_kgK": 1006.0,
        "mu_Pa_s": 1.85e-5,
        "k_W_mK": 0.026,
    },
    "Water-like coolant": {
        "cooling_method": "Direct-to-chip liquid cold plate",
        "rho_kg_m3": 997.0,
        "cp_J_kgK": 4180.0,
        "mu_Pa_s": 8.90e-4,
        "k_W_mK": 0.60,
    },
    "Representative dielectric liquid": {
        "cooling_method": "Single-phase dielectric immersion",
        "rho_kg_m3": 1400.0,
        "cp_J_kgK": 1500.0,
        "mu_Pa_s": 4.00e-3,
        "k_W_mK": 0.12,
    },
}


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def coolant_flow_for_heat_load(Q_W, cp_J_kgK, rho_kg_m3, delta_T_K):
    """
    Calculate coolant mass flow and volume flow required to carry heat load Q
    for a specified bulk coolant temperature rise.
    """
    mdot_kg_s = Q_W / (cp_J_kgK * delta_T_K)
    vdot_m3_s = mdot_kg_s / rho_kg_m3
    vdot_L_min = vdot_m3_s * 1000.0 * 60.0
    vdot_CFM = vdot_m3_s * 2118.880003
    return mdot_kg_s, vdot_m3_s, vdot_L_min, vdot_CFM


def reynolds_number(rho, velocity, length, mu):
    return rho * velocity * length / mu


def prandtl_number(cp, mu, k):
    return cp * mu / k


def laminar_flat_plate_average_nusselt(Re_L, Pr):
    """
    Average laminar flat-plate forced convection screening correlation:
    Nu_L = 0.664 Re_L^0.5 Pr^(1/3)

    Used only as a first-pass estimate for external forced convection.
    """
    return 0.664 * math.sqrt(Re_L) * (Pr ** (1.0 / 3.0))


def convective_resistance(h_W_m2K, area_m2):
    return 1.0 / (h_W_m2K * area_m2)


def surface_to_fluid_delta_T(Q_W, h_W_m2K, area_m2):
    return Q_W / (h_W_m2K * area_m2)


def straight_fin_efficiency(h_W_m2K, k_fin_W_mK, thickness_m, height_m):
    """
    Straight rectangular fin efficiency approximation:
    eta = tanh(mL) / (mL)
    m = sqrt(2h / (k t))

    This assumes a thin rectangular fin with convection from both large faces.
    It is a screening estimate only.
    """
    m = math.sqrt(2.0 * h_W_m2K / (k_fin_W_mK * thickness_m))
    mL = m * height_m
    if mL == 0:
        return 1.0
    return math.tanh(mL) / mL


def cold_plate_nusselt_number(Re, Pr):
    """
    Screening Nusselt number choice for the simple rectangular minichannel.

    For Re < 2300:
        Uses a constant rectangular-duct laminar screening value, Nu = 4.12.
        This represents a simplified fully developed laminar assumption.

    For 2300 <= Re <= 4000:
        Uses a transition screening estimate.

    For Re > 4000:
        Uses Dittus-Boelter turbulent internal-flow estimate.

    Important limitation:
        For short minichannels, thermal entrance effects may be important.
        This function does not model developing-flow enhancement.
    """
    if Re < 2300:
        Nu = 4.12
        regime = "Laminar"
        correlation = "Rectangular-duct laminar screening value, Nu = 4.12"
    elif Re > 4000:
        Nu = 0.023 * (Re ** 0.8) * (Pr ** 0.4)
        regime = "Turbulent"
        correlation = "Dittus-Boelter turbulent internal-flow estimate"
    else:
        Nu_laminar = 4.12
        Nu_turbulent = 0.023 * (Re ** 0.8) * (Pr ** 0.4)
        Nu = 0.5 * (Nu_laminar + Nu_turbulent)
        regime = "Transitional screening"
        correlation = "Average of laminar rectangular-duct and Dittus-Boelter estimates"

    return Nu, regime, correlation


def laminar_thermal_entrance_length(Re, Pr, Dh_m):
    """
    Approximate laminar thermal entrance length:
    L_th ≈ 0.05 Re Pr Dh
    """
    return 0.05 * Re * Pr * Dh_m


# ============================================================
# 5. PART A: COOLANT HEAT-CARRYING CAPACITY
# ============================================================

flow_rows = []

for fluid_name, props in fluids.items():
    for dT in DELTA_T_COOLANT_LIST_K:
        mdot, vdot, L_min, CFM = coolant_flow_for_heat_load(
            Q_W=Q_W,
            cp_J_kgK=props["cp_J_kgK"],
            rho_kg_m3=props["rho_kg_m3"],
            delta_T_K=dT,
        )

        volumetric_heat_capacity_J_m3K = props["rho_kg_m3"] * props["cp_J_kgK"]

        flow_rows.append(
            {
                "cooling_method": props["cooling_method"],
                "fluid": fluid_name,
                "heat_load_W": Q_W,
                "coolant_delta_T_K": dT,
                "rho_kg_m3": props["rho_kg_m3"],
                "cp_J_kgK": props["cp_J_kgK"],
                "volumetric_heat_capacity_J_m3K": volumetric_heat_capacity_J_m3K,
                "mass_flow_kg_s": mdot,
                "volume_flow_m3_s": vdot,
                "volume_flow_L_min": L_min,
                "volume_flow_CFM": CFM,
            }
        )

flow_df = pd.DataFrame(flow_rows)

air_flow_by_dT = (
    flow_df[flow_df["fluid"] == "Air"]
    .set_index("coolant_delta_T_K")["volume_flow_m3_s"]
    .to_dict()
)

flow_df["air_to_case_volume_flow_ratio"] = flow_df.apply(
    lambda row: air_flow_by_dT[row["coolant_delta_T_K"]] / row["volume_flow_m3_s"],
    axis=1,
)

flow_csv = RESULTS_DIR / "flow_rate_comparison.csv"
flow_df.to_csv(flow_csv, index=False)


# ============================================================
# 6. PART B: DIRECT-TO-CHIP COLD-PLATE SCREENING
# ============================================================
# Simple minichannel cold plate:
# - active area around chip: 50 x 50 mm
# - 10 parallel rectangular channels
# - each channel: 2 mm wide x 1 mm high x 50 mm long
# - water-like coolant
# - flow rate based on 10 K coolant temperature rise
#
# This is not an optimized cold plate.
# Manifold losses, non-uniform flow distribution, contact resistance,
# spreading resistance, and pressure drop are not modelled.

water = fluids["Water-like coolant"]

cold_plate = {
    "case": "Direct-to-chip cold plate, minichannel screening",
    "fluid": "Water-like coolant",
    "number_of_channels": 10,
    "channel_width_m": 0.002,
    "channel_height_m": 0.001,
    "channel_length_m": 0.050,
    "coolant_delta_T_K": 10.0,
}

cp_mdot, cp_vdot, cp_L_min, cp_CFM = coolant_flow_for_heat_load(
    Q_W,
    water["cp_J_kgK"],
    water["rho_kg_m3"],
    cold_plate["coolant_delta_T_K"],
)

channel_area_m2 = cold_plate["channel_width_m"] * cold_plate["channel_height_m"]
total_flow_area_m2 = cold_plate["number_of_channels"] * channel_area_m2
channel_velocity_m_s = cp_vdot / total_flow_area_m2

channel_wetted_perimeter_m = 2.0 * (
    cold_plate["channel_width_m"] + cold_plate["channel_height_m"]
)

hydraulic_diameter_m = 4.0 * channel_area_m2 / channel_wetted_perimeter_m

Re_cold_plate = reynolds_number(
    water["rho_kg_m3"],
    channel_velocity_m_s,
    hydraulic_diameter_m,
    water["mu_Pa_s"],
)

Pr_cold_plate = prandtl_number(
    water["cp_J_kgK"],
    water["mu_Pa_s"],
    water["k_W_mK"],
)

Nu_cold_plate, cold_plate_regime, cold_plate_correlation = cold_plate_nusselt_number(
    Re_cold_plate,
    Pr_cold_plate,
)

h_cold_plate = Nu_cold_plate * water["k_W_mK"] / hydraulic_diameter_m

cold_plate_wetted_area_m2 = (
    cold_plate["number_of_channels"]
    * channel_wetted_perimeter_m
    * cold_plate["channel_length_m"]
)

R_conv_cold_plate_K_W = convective_resistance(
    h_cold_plate,
    cold_plate_wetted_area_m2,
)

dT_surface_fluid_cold_plate_K = surface_to_fluid_delta_T(
    Q_W,
    h_cold_plate,
    cold_plate_wetted_area_m2,
)

thermal_entrance_length_cold_plate_m = laminar_thermal_entrance_length(
    Re_cold_plate,
    Pr_cold_plate,
    hydraulic_diameter_m,
)

thermal_entrance_length_ratio = (
    thermal_entrance_length_cold_plate_m / cold_plate["channel_length_m"]
)


# ============================================================
# 7. PART B2: COLD-PLATE FLOW SENSITIVITY
# ============================================================
# This sensitivity varies the water-like coolant flow around the 10 K baseline case.
#
# Important:
# In the laminar branch, Nu is kept constant at 4.12.
# Therefore, h and surface-to-fluid DeltaT remain constant while the flow remains laminar.
# This is a limitation of the simplified fully developed laminar constant-Nu model.
# A real short minichannel may have developing-flow effects that are not modelled here.

cold_plate_flow_multiplier_list = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]

cold_plate_sensitivity_rows = []

for multiplier in cold_plate_flow_multiplier_list:
    vdot = cp_vdot * multiplier
    mdot = cp_mdot * multiplier

    equivalent_bulk_delta_T_K = Q_W / (mdot * water["cp_J_kgK"])
    velocity = vdot / total_flow_area_m2

    Re = reynolds_number(
        water["rho_kg_m3"],
        velocity,
        hydraulic_diameter_m,
        water["mu_Pa_s"],
    )

    Pr = Pr_cold_plate

    Nu, regime, correlation = cold_plate_nusselt_number(Re, Pr)
    h = Nu * water["k_W_mK"] / hydraulic_diameter_m
    R_conv = convective_resistance(h, cold_plate_wetted_area_m2)
    dT_surface_fluid = surface_to_fluid_delta_T(Q_W, h, cold_plate_wetted_area_m2)

    L_th = laminar_thermal_entrance_length(Re, Pr, hydraulic_diameter_m)
    L_th_ratio = L_th / cold_plate["channel_length_m"]

    cold_plate_sensitivity_rows.append(
        {
            "flow_multiplier_relative_to_10K_case": multiplier,
            "water_volume_flow_L_min": vdot * 1000.0 * 60.0,
            "equivalent_bulk_coolant_delta_T_K": equivalent_bulk_delta_T_K,
            "channel_velocity_m_s": velocity,
            "Re": Re,
            "Pr": Pr,
            "Nu": Nu,
            "h_W_m2K": h,
            "surface_to_fluid_delta_T_K": dT_surface_fluid,
            "flow_regime": regime,
            "correlation_used": correlation,
            "thermal_entrance_length_m": L_th,
            "thermal_entrance_length_to_channel_length_ratio": L_th_ratio,
            "note": "Laminar constant-Nu branch is simplified; developing-flow effects are not modelled.",
        }
    )

cold_plate_sensitivity_df = pd.DataFrame(cold_plate_sensitivity_rows)

cold_plate_sensitivity_csv = RESULTS_DIR / "cold_plate_flow_sensitivity.csv"
cold_plate_sensitivity_df.to_csv(cold_plate_sensitivity_csv, index=False)


# ============================================================
# 8. PART C: SINGLE-PHASE IMMERSION SCREENING
# ============================================================
# We use a representative dielectric liquid.
#
# Three immersion cases are included:
# C1: bare chip-area flat plate
# C2: idealized 80 x 80 mm spreader-only flat plate
# C3: idealized 80 x 80 mm finned immersed heat spreader
#
# The spreader/finned cases represent idealized heat-spreading concepts.
# Vapor-chamber internal resistance, wick limits, dry-out, orientation effects,
# fin-array pressure drop, non-uniform flow, and tank circulation are not modelled.

dielectric = fluids["Representative dielectric liquid"]

# Fixed dielectric volumetric flow supply for immersion cases.
# Baseline: flow corresponding to 10 K bulk coolant temperature rise.
dielectric_mdot_10K, dielectric_vdot_10K, dielectric_L_min_10K, dielectric_CFM_10K = coolant_flow_for_heat_load(
    Q_W,
    dielectric["cp_J_kgK"],
    dielectric["rho_kg_m3"],
    10.0,
)

IMMERSION_BASELINE_BULK_DELTA_T_K = 10.0

# Assumed flow passage height over immersed surface
IMMERSION_FLOW_GAP_M = 0.010  # 10 mm

Pr_immersion = prandtl_number(
    dielectric["cp_J_kgK"],
    dielectric["mu_Pa_s"],
    dielectric["k_W_mK"],
)

# C1: bare 45 x 45 mm immersion
bare_length_m = 0.045
bare_width_m = 0.045
bare_area_m2 = bare_length_m * bare_width_m
bare_flow_area_m2 = bare_width_m * IMMERSION_FLOW_GAP_M
bare_velocity_m_s = dielectric_vdot_10K / bare_flow_area_m2

Re_immersion_bare = reynolds_number(
    dielectric["rho_kg_m3"],
    bare_velocity_m_s,
    bare_length_m,
    dielectric["mu_Pa_s"],
)

Nu_immersion_bare = laminar_flat_plate_average_nusselt(
    Re_immersion_bare,
    Pr_immersion,
)

h_immersion_bare = Nu_immersion_bare * dielectric["k_W_mK"] / bare_length_m

R_conv_immersion_bare_K_W = convective_resistance(
    h_immersion_bare,
    bare_area_m2,
)

dT_surface_fluid_immersion_bare_K = surface_to_fluid_delta_T(
    Q_W,
    h_immersion_bare,
    bare_area_m2,
)


# C2: idealized 80 x 80 mm spreader-only immersion
spreader_length_m = 0.080
spreader_width_m = 0.080
spreader_area_m2 = spreader_length_m * spreader_width_m
spreader_flow_area_m2 = spreader_width_m * IMMERSION_FLOW_GAP_M
spreader_velocity_m_s = dielectric_vdot_10K / spreader_flow_area_m2

Re_immersion_spreader = reynolds_number(
    dielectric["rho_kg_m3"],
    spreader_velocity_m_s,
    spreader_length_m,
    dielectric["mu_Pa_s"],
)

Nu_immersion_spreader = laminar_flat_plate_average_nusselt(
    Re_immersion_spreader,
    Pr_immersion,
)

h_immersion_spreader = (
    Nu_immersion_spreader * dielectric["k_W_mK"] / spreader_length_m
)

R_conv_immersion_spreader_K_W = convective_resistance(
    h_immersion_spreader,
    spreader_area_m2,
)

dT_surface_fluid_immersion_spreader_K = surface_to_fluid_delta_T(
    Q_W,
    h_immersion_spreader,
    spreader_area_m2,
)


# C3: idealized finned immersion spreader
# Geometry:
# - 80 x 80 mm spreader footprint
# - straight aluminium fins
# - fin height: 10 mm
# - fin thickness: 1 mm
# - fin pitch: 4 mm
# - fin length: 80 mm
# - about 20 fins over 80 mm width
#
# Fin efficiency is included.
# The same external-flow h from the spreader case is used as a first-pass
# approximation for fin surfaces.
# Real inter-fin channel convection is not resolved.

ALUMINIUM_K_W_MK = 200.0

fin_height_m = 0.010
fin_thickness_m = 0.001
fin_pitch_m = 0.004
fin_length_m = 0.080
number_of_fins = int(spreader_width_m / fin_pitch_m)

fin_side_area_per_fin_m2 = 2.0 * fin_height_m * fin_length_m
fin_tip_area_per_fin_m2 = fin_thickness_m * fin_length_m
total_fin_area_m2 = number_of_fins * (fin_side_area_per_fin_m2 + fin_tip_area_per_fin_m2)

fin_footprint_area_m2 = number_of_fins * fin_thickness_m * fin_length_m
exposed_base_area_m2 = max(spreader_area_m2 - fin_footprint_area_m2, 0.0)

fin_eta = straight_fin_efficiency(
    h_W_m2K=h_immersion_spreader,
    k_fin_W_mK=ALUMINIUM_K_W_MK,
    thickness_m=fin_thickness_m,
    height_m=fin_height_m,
)

effective_finned_area_m2 = exposed_base_area_m2 + fin_eta * total_fin_area_m2

h_immersion_finned = h_immersion_spreader

R_conv_immersion_finned_K_W = convective_resistance(
    h_immersion_finned,
    effective_finned_area_m2,
)

dT_surface_fluid_immersion_finned_K = surface_to_fluid_delta_T(
    Q_W,
    h_immersion_finned,
    effective_finned_area_m2,
)


# ============================================================
# 9. H / CONVECTIVE SCREENING SUMMARY
# ============================================================

h_rows = [
    {
        "case": "Air cooling CFD-3 reference",
        "fluid": "Air",
        "model_type": "System-level ANSYS Fluent CHT reference",
        "geometry_basis": "80 x 120 x 35 mm ducted air-cooled heatsink",
        "velocity_m_s": 5.0,
        "Re": None,
        "Pr": None,
        "Nu": None,
        "h_W_m2K": None,
        "heat_transfer_area_m2": None,
        "effective_heat_transfer_area_m2": None,
        "R_conv_K_W": None,
        "surface_to_fluid_delta_T_K": None,
        "max_chip_temperature_C": AIR_CFD3_T_CHIP_MAX_C,
        "chip_rise_above_inlet_K": AIR_CFD3_CHIP_RISE_ABOVE_INLET_K,
        "pressure_drop_Pa": AIR_CFD3_PRESSURE_DROP_PA,
        "main_interpretation": "Contextual system-level air-cooled CFD reference, not a component-level convection bar",
    },
    {
        "case": "Direct-to-chip cold plate",
        "fluid": "Water-like coolant",
        "model_type": "Internal minichannel forced convection",
        "geometry_basis": "10 rectangular channels, 2 mm x 1 mm x 50 mm",
        "velocity_m_s": channel_velocity_m_s,
        "Re": Re_cold_plate,
        "Pr": Pr_cold_plate,
        "Nu": Nu_cold_plate,
        "h_W_m2K": h_cold_plate,
        "heat_transfer_area_m2": cold_plate_wetted_area_m2,
        "effective_heat_transfer_area_m2": cold_plate_wetted_area_m2,
        "R_conv_K_W": R_conv_cold_plate_K_W,
        "surface_to_fluid_delta_T_K": dT_surface_fluid_cold_plate_K,
        "max_chip_temperature_C": None,
        "chip_rise_above_inlet_K": None,
        "pressure_drop_Pa": None,
        "main_interpretation": "Simple minichannel cold-plate baseline, not optimized",
    },
    {
        "case": "Bare immersion flat plate",
        "fluid": "Representative dielectric liquid",
        "model_type": "Laminar external forced convection",
        "geometry_basis": "Bare 45 x 45 mm heated chip footprint",
        "velocity_m_s": bare_velocity_m_s,
        "Re": Re_immersion_bare,
        "Pr": Pr_immersion,
        "Nu": Nu_immersion_bare,
        "h_W_m2K": h_immersion_bare,
        "heat_transfer_area_m2": bare_area_m2,
        "effective_heat_transfer_area_m2": bare_area_m2,
        "R_conv_K_W": R_conv_immersion_bare_K_W,
        "surface_to_fluid_delta_T_K": dT_surface_fluid_immersion_bare_K,
        "max_chip_temperature_C": None,
        "chip_rise_above_inlet_K": None,
        "pressure_drop_Pa": None,
        "main_interpretation": "Conservative bare-surface immersion reference",
    },
    {
        "case": "Spreader-only immersion flat plate",
        "fluid": "Representative dielectric liquid",
        "model_type": "Laminar external forced convection with idealized spreading area",
        "geometry_basis": "Idealized 80 x 80 mm heat-spreader footprint",
        "velocity_m_s": spreader_velocity_m_s,
        "Re": Re_immersion_spreader,
        "Pr": Pr_immersion,
        "Nu": Nu_immersion_spreader,
        "h_W_m2K": h_immersion_spreader,
        "heat_transfer_area_m2": spreader_area_m2,
        "effective_heat_transfer_area_m2": spreader_area_m2,
        "R_conv_K_W": R_conv_immersion_spreader_K_W,
        "surface_to_fluid_delta_T_K": dT_surface_fluid_immersion_spreader_K,
        "max_chip_temperature_C": None,
        "chip_rise_above_inlet_K": None,
        "pressure_drop_Pa": None,
        "main_interpretation": "Shows heat spreading alone under same dielectric flow supply",
    },
    {
        "case": "Finned immersion heat spreader",
        "fluid": "Representative dielectric liquid",
        "model_type": "Idealized effective-area immersion concept with fin efficiency",
        "geometry_basis": "80 x 80 mm spreader, 20 aluminium fins, 10 mm high, 4 mm pitch",
        "velocity_m_s": spreader_velocity_m_s,
        "Re": Re_immersion_spreader,
        "Pr": Pr_immersion,
        "Nu": Nu_immersion_spreader,
        "h_W_m2K": h_immersion_finned,
        "heat_transfer_area_m2": exposed_base_area_m2 + total_fin_area_m2,
        "effective_heat_transfer_area_m2": effective_finned_area_m2,
        "R_conv_K_W": R_conv_immersion_finned_K_W,
        "surface_to_fluid_delta_T_K": dT_surface_fluid_immersion_finned_K,
        "max_chip_temperature_C": None,
        "chip_rise_above_inlet_K": None,
        "pressure_drop_Pa": None,
        "main_interpretation": "Shows benefit of enhanced immersed wetted area, still idealized",
    },
]

h_df = pd.DataFrame(h_rows)

h_csv = RESULTS_DIR / "h_screening_summary.csv"
h_df.to_csv(h_csv, index=False)


# ============================================================
# 10. IMMERSION DIRECTED-FLOW SENSITIVITY
# ============================================================

velocity_rows = []

dielectric_flow_multiplier_list = [0.5, 1.0, 2.0, 4.0]

for multiplier in dielectric_flow_multiplier_list:
    dielectric_vdot = dielectric_vdot_10K * multiplier
    dielectric_mdot = dielectric_mdot_10K * multiplier
    equivalent_bulk_delta_T_K = Q_W / (dielectric_mdot * dielectric["cp_J_kgK"])

    for label, length, width, area in [
        ("Bare 45 x 45 mm immersion", bare_length_m, bare_width_m, bare_area_m2),
        ("Spreader-only 80 x 80 mm immersion", spreader_length_m, spreader_width_m, spreader_area_m2),
        ("Finned immersion heat spreader", spreader_length_m, spreader_width_m, effective_finned_area_m2),
    ]:
        flow_area = width * IMMERSION_FLOW_GAP_M
        velocity = dielectric_vdot / flow_area

        Re = reynolds_number(
            dielectric["rho_kg_m3"],
            velocity,
            length,
            dielectric["mu_Pa_s"],
        )

        Nu = laminar_flat_plate_average_nusselt(Re, Pr_immersion)
        h = Nu * dielectric["k_W_mK"] / length

        R_conv = convective_resistance(h, area)
        dT = surface_to_fluid_delta_T(Q_W, h, area)

        velocity_rows.append(
            {
                "case": label,
                "dielectric_flow_multiplier_relative_to_10K_case": multiplier,
                "dielectric_volume_flow_L_min": dielectric_vdot * 1000.0 * 60.0,
                "equivalent_bulk_coolant_delta_T_K": equivalent_bulk_delta_T_K,
                "velocity_m_s": velocity,
                "Re": Re,
                "Pr": Pr_immersion,
                "Nu": Nu,
                "h_W_m2K": h,
                "effective_area_m2": area,
                "R_conv_K_W": R_conv,
                "surface_to_fluid_delta_T_K": dT,
                "note": "Flow cases are sensitivity points around the assumed 10 K bulk-rise baseline, not pump-selected operating points.",
            }
        )

velocity_df = pd.DataFrame(velocity_rows)

velocity_csv = RESULTS_DIR / "immersion_velocity_sensitivity.csv"
velocity_df.to_csv(velocity_csv, index=False)


# ============================================================
# 11. PLOTS
# ============================================================

# Plot A: volume-flow comparison at 10 K
flow_10K = flow_df[flow_df["coolant_delta_T_K"] == 10.0].copy()

plt.figure(figsize=(8, 5))
plt.bar(flow_10K["fluid"], flow_10K["volume_flow_L_min"])
plt.yscale("log")
plt.ylabel("Required volume flow rate (L/min, log scale)")
plt.xlabel("Coolant")
plt.title("Coolant Flow Required to Carry 250 W at 10 K Bulk Temperature Rise")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
flow_fig = FIGURES_DIR / "liquid_cooling_flow_comparison.png"
plt.savefig(flow_fig, dpi=200)
plt.close()


# Plot B: component-level surface-to-fluid delta-T comparison
# Air CFD-3 is added as a dashed contextual reference line because it is system-level,
# not the same type of component-level convective estimate.
h_plot_df = h_df[h_df["surface_to_fluid_delta_T_K"].notna()].copy()

plt.figure(figsize=(10, 5))
plt.bar(h_plot_df["case"], h_plot_df["surface_to_fluid_delta_T_K"])
plt.axhline(
    AIR_CFD3_CHIP_RISE_ABOVE_INLET_K,
    linestyle="--",
    linewidth=1.5,
    label="CFD-3 air-cooled chip rise above inlet, system-level reference",
)
plt.yscale("log")
plt.ylabel("Estimated surface-to-fluid temperature rise (K, log scale)")
plt.xlabel("Component-level screening case")
plt.title("Convective Screening: Surface Area and Architecture Effects")
plt.xticks(rotation=25, ha="right")
plt.legend()
plt.tight_layout()
h_fig = FIGURES_DIR / "liquid_cooling_h_comparison.png"
plt.savefig(h_fig, dpi=200)
plt.close()


# Plot C: cold-plate flow sensitivity
plt.figure(figsize=(8, 5))
plt.plot(
    cold_plate_sensitivity_df["water_volume_flow_L_min"],
    cold_plate_sensitivity_df["surface_to_fluid_delta_T_K"],
    marker="o",
)
plt.xscale("log")
plt.yscale("log")
plt.ylabel("Estimated surface-to-fluid temperature rise (K, log scale)")
plt.xlabel("Water-like coolant flow rate (L/min, log scale)")
plt.title("Cold-Plate Flow Sensitivity Under Simplified Nu Model")
plt.tight_layout()
cold_plate_fig = FIGURES_DIR / "cold_plate_flow_sensitivity.png"
plt.savefig(cold_plate_fig, dpi=200)
plt.close()


# ============================================================
# 12. PRINT SUMMARY
# ============================================================

pd.set_option("display.width", 240)
pd.set_option("display.max_columns", 50)

print("=" * 100)
print("LIQUID AND IMMERSION COOLING SCREENING EXTENSION")
print("=" * 100)

print("\nPART A: COOLANT FLOW RATE COMPARISON")
print(flow_df[[
    "fluid",
    "coolant_delta_T_K",
    "mass_flow_kg_s",
    "volume_flow_L_min",
    "volume_flow_CFM",
    "air_to_case_volume_flow_ratio",
]].to_string(index=False))

print("\nPART B: CONVECTIVE HEAT-TRANSFER SCREENING")
print(h_df[[
    "case",
    "fluid",
    "model_type",
    "velocity_m_s",
    "Re",
    "Pr",
    "Nu",
    "h_W_m2K",
    "effective_heat_transfer_area_m2",
    "surface_to_fluid_delta_T_K",
]].to_string(index=False))

print("\nPART C: COLD-PLATE FLOW SENSITIVITY")
print(cold_plate_sensitivity_df[[
    "flow_multiplier_relative_to_10K_case",
    "water_volume_flow_L_min",
    "equivalent_bulk_coolant_delta_T_K",
    "channel_velocity_m_s",
    "Re",
    "Nu",
    "h_W_m2K",
    "surface_to_fluid_delta_T_K",
    "flow_regime",
    "thermal_entrance_length_to_channel_length_ratio",
]].to_string(index=False))

print("\nPART D: IMMERSION DIRECTED-FLOW SENSITIVITY")
print(velocity_df[[
    "case",
    "dielectric_flow_multiplier_relative_to_10K_case",
    "dielectric_volume_flow_L_min",
    "equivalent_bulk_coolant_delta_T_K",
    "velocity_m_s",
    "Re",
    "Nu",
    "h_W_m2K",
    "surface_to_fluid_delta_T_K",
]].to_string(index=False))

print("\nHand-check values:")
print(f"- Chip area = {CHIP_AREA_M2:.6f} m^2")
print(f"- Chip heat flux = {Q_W / CHIP_AREA_M2:.0f} W/m^2 = {(Q_W / CHIP_AREA_M2) / 10000:.2f} W/cm^2")
print(f"- Cold plate hydraulic diameter = {hydraulic_diameter_m * 1000:.3f} mm")
print(f"- Cold plate Re = {Re_cold_plate:.1f}, regime = {cold_plate_regime}")
print(f"- Cold plate thermal entrance length = {thermal_entrance_length_cold_plate_m * 1000:.1f} mm")
print(f"- Cold plate channel length = {cold_plate['channel_length_m'] * 1000:.1f} mm")
print(f"- Cold plate entrance-length/channel-length ratio = {thermal_entrance_length_ratio:.2f}")
print(f"- Cold plate h = {h_cold_plate:.1f} W/m^2K")
print(f"- Cold plate surface-to-fluid DeltaT = {dT_surface_fluid_cold_plate_K:.1f} K")
print(f"- Bare immersion velocity at baseline dielectric flow = {bare_velocity_m_s:.4f} m/s")
print(f"- Spreader immersion velocity at baseline dielectric flow = {spreader_velocity_m_s:.4f} m/s")
print(f"- Immersion fin efficiency = {fin_eta:.3f}")
print(f"- Finned immersion effective area = {effective_finned_area_m2:.5f} m^2")
print(f"- Finned immersion surface-to-fluid DeltaT = {dT_surface_fluid_immersion_finned_K:.1f} K")
print(f"- CFD-3 air-cooled chip rise above inlet = {AIR_CFD3_CHIP_RISE_ABOVE_INLET_K:.2f} K")

print("\nSaved files:")
print(f"- {flow_csv}")
print(f"- {h_csv}")
print(f"- {cold_plate_sensitivity_csv}")
print(f"- {velocity_csv}")
print(f"- {flow_fig}")
print(f"- {h_fig}")
print(f"- {cold_plate_fig}")

print("\nKey interpretation:")
print("1. Liquid coolants require much lower volumetric flow than air for the same 250 W heat load.")
print("2. Coolant heat-carrying capacity alone does not predict chip temperature.")
print("3. The cold-plate baseline is laminar and uses a simplified fully developed rectangular-duct Nu value.")
print("4. The cold-plate thermal entrance length is larger than the channel length, so developing-flow effects may matter.")
print("5. Bare chip-area immersion is a conservative lower-bound reference and is not sufficient for this heat flux.")
print("6. Spreading the heat helps, but a flat spreader alone is still limited under the assumed dielectric flow supply.")
print("7. Adding fins and accounting for fin efficiency greatly reduces the estimated surface-to-fluid temperature rise.")
print("8. Air CFD-3 is kept as a system-level reference, not a directly equivalent component-level convection estimate.")
print("9. This is screening only, not validated liquid-cooling or immersion-cooling product design.")