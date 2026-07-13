"""
First-order thermal resistance model for a simplified 250 W PCIe AI accelerator card.

Project:
Mechanical and Thermal Design Workflow for a 250 W PCIe AI Accelerator Card

Purpose:
This script estimates the required chip-to-air thermal resistance and calculates
a first-order chip temperature estimate using a simplified thermal resistance path.

Main thermal path:
Chip/package -> TIM -> heatsink/spreader -> fins -> forced air

This is not a replacement for CFD. It is a first-principles sizing calculation
used before detailed simulation.
"""

# ------------------------------------------------------------
# 1. Baseline design inputs
# ------------------------------------------------------------

# Temperatures
T_air_inlet_C = 25.0          # inlet air temperature [degC]
T_chip_target_C = 85.0       # target maximum chip case temperature [degC]

# Chip power
Q_chip_W = 250.0             # main accelerator chip power [W]

# Chip geometry
chip_length_m = 45e-3        # chip length [m]
chip_width_m = 45e-3         # chip width [m]
A_chip_m2 = chip_length_m * chip_width_m

# Baseline TIM properties
t_TIM_m = 0.2e-3             # TIM bond-line thickness [m]
k_TIM_W_mK = 6.0             # TIM thermal conductivity [W/mK]

# Assumed non-TIM thermal resistance
# This represents package/spreading/heatsink-to-air contribution.
# It is an engineering placeholder for first-order sizing.
R_non_TIM_K_W = 0.18         # [K/W]


# ------------------------------------------------------------
# 2. Required chip-to-air thermal resistance
# ------------------------------------------------------------

delta_T_allowed_K = T_chip_target_C - T_air_inlet_C

R_required_K_W = delta_T_allowed_K / Q_chip_W


# ------------------------------------------------------------
# 3. TIM thermal resistance
# ------------------------------------------------------------

R_TIM_K_W = t_TIM_m / (k_TIM_W_mK * A_chip_m2)


# ------------------------------------------------------------
# 4. Total first-order thermal resistance
# ------------------------------------------------------------

R_total_K_W = R_TIM_K_W + R_non_TIM_K_W

T_chip_estimated_C = T_air_inlet_C + Q_chip_W * R_total_K_W

thermal_margin_C = T_chip_target_C - T_chip_estimated_C


# ------------------------------------------------------------
# 5. Print results
# ------------------------------------------------------------

print("============================================================")
print("PCIe AI Accelerator First-Order Thermal Resistance Model")
print("============================================================")

print(f"Inlet air temperature               : {T_air_inlet_C:.1f} degC")
print(f"Target maximum chip temperature     : {T_chip_target_C:.1f} degC")
print(f"Chip power                          : {Q_chip_W:.1f} W")
print(f"Allowed chip temperature rise       : {delta_T_allowed_K:.1f} K")

print("------------------------------------------------------------")
print("Required Thermal Resistance")
print("------------------------------------------------------------")
print(f"Required chip-to-air Rth            : {R_required_K_W:.3f} K/W")

print("------------------------------------------------------------")
print("TIM Calculation")
print("------------------------------------------------------------")
print(f"Chip area                           : {A_chip_m2:.6f} m^2")
print(f"TIM thickness                       : {t_TIM_m*1e3:.3f} mm")
print(f"TIM conductivity                    : {k_TIM_W_mK:.1f} W/mK")
print(f"TIM thermal resistance              : {R_TIM_K_W:.4f} K/W")

print("------------------------------------------------------------")
print("First-Order Temperature Estimate")
print("------------------------------------------------------------")
print(f"Assumed non-TIM Rth                 : {R_non_TIM_K_W:.3f} K/W")
print(f"Total estimated Rth                 : {R_total_K_W:.3f} K/W")
print(f"Estimated chip temperature          : {T_chip_estimated_C:.1f} degC")
print(f"Thermal margin to target            : {thermal_margin_C:.1f} degC")

print("------------------------------------------------------------")
if T_chip_estimated_C <= T_chip_target_C:
    print("Status                              : PASS for first-order estimate")
else:
    print("Status                              : FAIL for first-order estimate")
print("============================================================")