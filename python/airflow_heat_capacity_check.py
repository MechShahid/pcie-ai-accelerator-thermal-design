"""
Airflow heat-capacity and flow-regime sanity check for a simplified
250 W PCIe AI accelerator card.

Purpose:
Before CAD and CFD, estimate whether the assumed airflow velocities can carry away
the chip-only and full-board heat loads without excessive air temperature rise.

This script also estimates:
- Volumetric flow rate in CFM and m^3/h
- Reynolds number based on heatsink fin-channel hydraulic diameter
- Dynamic pressure
- Basic flow-regime indication

Main energy balance:
Q = m_dot * cp * Delta_T

Mass flow:
m_dot = rho_air * velocity * flow_area

Reynolds number:
Re = rho_air * velocity * Dh / mu_air

Hydraulic diameter for rectangular fin channel:
Dh = 2ab / (a + b)

where:
a = fin spacing
b = fin height

This does not replace CFD. It is a first-order sanity check to catch
unrealistic airflow assumptions early.
"""

import csv
import os

# ------------------------------------------------------------
# 1. Air properties and thermal inputs
# ------------------------------------------------------------

rho_air_kg_m3 = 1.184       # air density near 25 C [kg/m^3]
cp_air_J_kgK = 1007.0       # air specific heat [J/kgK]
mu_air_Pa_s = 1.85e-5       # dynamic viscosity of air near 25 C [Pa.s]

T_air_inlet_C = 25.0

# Heat loads
Q_chip_W = 250.0
Q_full_board_W = 320.0

# Airflow velocity cases
velocity_cases_m_s = [1.0, 2.0, 3.0, 4.0]

# ------------------------------------------------------------
# 2. Heatsink / flow-area assumptions
# ------------------------------------------------------------

# Heatsink dimensions
fin_height_m = 25e-3
heatsink_width_m = 80e-3

# Fin-channel dimensions for Reynolds number
fin_spacing_m = 2e-3
channel_height_m = fin_height_m

# Hydraulic diameter for one rectangular channel approximation
D_h_m = 2.0 * fin_spacing_m * channel_height_m / (
    fin_spacing_m + channel_height_m
)

# Conservative local heatsink frontal estimate:
# fin height x heatsink width
A_heatsink_frontal_m2 = fin_height_m * heatsink_width_m

# Larger board-level flow window estimate:
# card height x approximate open flow height around card
card_height_m = 111.15e-3
open_flow_height_m = 25e-3
A_board_flow_m2 = card_height_m * open_flow_height_m

flow_area_cases = [
    ("Local heatsink frontal area", A_heatsink_frontal_m2),
    ("Larger board-level flow window", A_board_flow_m2),
]

heat_load_cases = [
    ("Chip only", Q_chip_W),
    ("Full board", Q_full_board_W),
]

# ------------------------------------------------------------
# 3. Helper functions
# ------------------------------------------------------------

def classify_air_temperature_rise(delta_T_air_K):
    """Classify air temperature rise."""
    if delta_T_air_K <= 20.0:
        return "Good"
    elif delta_T_air_K <= 40.0:
        return "Caution"
    else:
        return "High rise"


def classify_reynolds_number(Re):
    """
    Basic internal-flow regime indication.

    For internal duct flow:
    Re < 2300 is commonly treated as laminar.
    2300-4000 is transitional.
    Re > 4000 is turbulent.

    For short heatsink fin channels, entrance effects, fan turbulence,
    bypass flow and geometry can change the real flow structure.
    This is only a first-order indicator.
    """
    if Re < 2300:
        return "Laminar indicator"
    elif Re < 4000:
        return "Transitional indicator"
    else:
        return "Turbulent indicator"


# ------------------------------------------------------------
# 4. Calculate airflow heat-capacity and flow-regime results
# ------------------------------------------------------------

results = []

for area_name, flow_area_m2 in flow_area_cases:
    for heat_name, Q_W in heat_load_cases:
        for velocity_m_s in velocity_cases_m_s:

            volumetric_flow_m3_s = velocity_m_s * flow_area_m2
            volumetric_flow_CFM = volumetric_flow_m3_s * 2118.88
            volumetric_flow_m3_h = volumetric_flow_m3_s * 3600.0

            mass_flow_kg_s = rho_air_kg_m3 * volumetric_flow_m3_s

            delta_T_air_K = Q_W / (mass_flow_kg_s * cp_air_J_kgK)
            T_air_outlet_C = T_air_inlet_C + delta_T_air_K

            Re_Dh = rho_air_kg_m3 * velocity_m_s * D_h_m / mu_air_Pa_s

            dynamic_pressure_Pa = 0.5 * rho_air_kg_m3 * velocity_m_s**2

            thermal_status = classify_air_temperature_rise(delta_T_air_K)
            re_status = classify_reynolds_number(Re_Dh)

            results.append({
                "flow_area_case": area_name,
                "heat_load_case": heat_name,
                "flow_area_m2": flow_area_m2,
                "velocity_m_s": velocity_m_s,
                "volumetric_flow_m3_s": volumetric_flow_m3_s,
                "volumetric_flow_CFM": volumetric_flow_CFM,
                "volumetric_flow_m3_h": volumetric_flow_m3_h,
                "mass_flow_kg_s": mass_flow_kg_s,
                "heat_load_W": Q_W,
                "delta_T_air_K": delta_T_air_K,
                "T_air_outlet_C": T_air_outlet_C,
                "Re_Dh": Re_Dh,
                "dynamic_pressure_Pa": dynamic_pressure_Pa,
                "thermal_status": thermal_status,
                "re_status": re_status,
            })

# ------------------------------------------------------------
# 5. Print summary
# ------------------------------------------------------------

print("============================================================")
print("Airflow Heat-Capacity and Flow-Regime Sanity Check")
print("============================================================")
print(f"Air density                         : {rho_air_kg_m3:.3f} kg/m^3")
print(f"Air specific heat                   : {cp_air_J_kgK:.1f} J/kgK")
print(f"Air dynamic viscosity               : {mu_air_Pa_s:.2e} Pa.s")
print(f"Inlet air temperature               : {T_air_inlet_C:.1f} degC")
print("------------------------------------------------------------")
print(f"Fin spacing                         : {fin_spacing_m*1e3:.2f} mm")
print(f"Fin/channel height                  : {channel_height_m*1e3:.2f} mm")
print(f"Hydraulic diameter, Dh              : {D_h_m*1e3:.2f} mm")
print(f"Heatsink frontal area               : {A_heatsink_frontal_m2:.6f} m^2")
print(f"Board-level flow window area        : {A_board_flow_m2:.6f} m^2")
print("------------------------------------------------------------")
print("Note:")
print("Re is estimated using fin-channel hydraulic diameter.")
print("This is a first-order indicator only. CFD will be used later")
print("to evaluate actual flow structure, bypass and pressure drop.")
print("============================================================")

print(
    f"{'Flow area case':<32}"
    f"{'Heat case':<12}"
    f"{'V [m/s]':>8}"
    f"{'CFM':>10}"
    f"{'m3/h':>10}"
    f"{'m_dot':>10}"
    f"{'Q [W]':>8}"
    f"{'dT_air':>10}"
    f"{'T_out':>10}"
    f"{'Re_Dh':>10}"
    f"{'q_dyn':>10}"
    f"{'Thermal':>12}"
    f"{'Re note':>24}"
)

print("-" * 176)

for row in results:
    print(
        f"{row['flow_area_case']:<32}"
        f"{row['heat_load_case']:<12}"
        f"{row['velocity_m_s']:>8.1f}"
        f"{row['volumetric_flow_CFM']:>10.1f}"
        f"{row['volumetric_flow_m3_h']:>10.1f}"
        f"{row['mass_flow_kg_s']:>10.5f}"
        f"{row['heat_load_W']:>8.1f}"
        f"{row['delta_T_air_K']:>10.1f}"
        f"{row['T_air_outlet_C']:>10.1f}"
        f"{row['Re_Dh']:>10.0f}"
        f"{row['dynamic_pressure_Pa']:>10.1f}"
        f"{row['thermal_status']:>12}"
        f"{row['re_status']:>24}"
    )

print("============================================================")

# ------------------------------------------------------------
# 6. Save CSV results
# ------------------------------------------------------------

os.makedirs("results", exist_ok=True)

csv_path = os.path.join("results", "airflow_heat_capacity_check.csv")

with open(csv_path, mode="w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "flow_area_case",
            "heat_load_case",
            "flow_area_m2",
            "velocity_m_s",
            "volumetric_flow_m3_s",
            "volumetric_flow_CFM",
            "volumetric_flow_m3_h",
            "mass_flow_kg_s",
            "heat_load_W",
            "delta_T_air_K",
            "T_air_outlet_C",
            "Re_Dh",
            "dynamic_pressure_Pa",
            "thermal_status",
            "re_status",
        ],
    )
    writer.writeheader()
    writer.writerows(results)

print(f"CSV results saved to: {csv_path}")