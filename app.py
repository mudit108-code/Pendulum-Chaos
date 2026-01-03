import streamlit as st
import numpy as np

from physics import simulate
from visualization import *

st.set_page_config(page_title="Chaotic Pendulum Simulation", layout="wide")

st.sidebar.title("Navigation")

section = st.sidebar.selectbox(
    "Go to Section",
    [
        "About the Topic",
        "Simulation Controls",
        "Mathematical Model & Equations",
        "Results & Plots",
    ]
)

# ================= ABOUT ================= #
if section == "About the Topic":
    st.title("📘 Chaotic Pendulum Simulation")

    st.markdown("""
### Physical Phenomenon:
A double pendulum is a classical mechanical system that exhibits
**deterministic chaos**, where very small differences in initial
conditions result in drastically different trajectories.

### Why Parameter Limits Exist?
- **Mass (kg):** Realistic laboratory scale systems
- **Angle (rad):** Physical motion constrained to ±π
- **Time (s):** Longer simulations increase numerical error and cost
                
### Parameters Explained:
- **θ (theta):** Angular displacement
- **ω (omega):** Angular velocity
- **Phase Space:** Shows chaos and non-periodicity
- **Energy Plot:** Validates numerical stability

### What This Simulation Demonstrates:
- Nonlinear dynamics
- Sensitivity to initial conditions
- Energy conservation (numerical validation)
""")

# ================= CONTROLS ================= #
elif section == "Simulation Controls":
    st.title("⚙️ Simulation Controls")

    mode = st.radio("Input Mode", ["Slider", "Manual"])

    def param(label, minv, maxv, default):
        if mode == "Slider":
            return st.slider(label, minv, maxv, default)
        return st.number_input(label, value=float(default))

    m1 = param("Mass 1 (kg)", 0.5, 5.0, 1.0)
    m2 = param("Mass 2 (kg)", 0.5, 5.0, 1.0)
    L1 = param("Length 1 (m)", 0.5, 3.0, 1.0)
    L2 = param("Length 2 (m)", 0.5, 3.0, 1.0)

    t1 = param("Initial θ₁ (rad)", -np.pi, np.pi, np.pi / 2)
    t2 = param("Initial θ₂ (rad)", -np.pi, np.pi, np.pi / 2)

    tmax = param("Simulation Time (s)", 5, 60, 20)

    if st.button("Run Simulation"):
        st.session_state["data"] = simulate(m1, m2, L1, L2, t1, t2, tmax)
        st.session_state["params"] = (m1, m2, L1, L2, t1, t2, tmax)
        st.success("Simulation executed successfully.")

# ================= MATHEMATICAL MODEL ================= #
elif section == "Mathematical Model & Equations":
    st.title("📐 Mathematical Model & Computation")

    if "data" not in st.session_state:
        st.warning("Run the simulation first.")
    else:
        m1, m2, L1, L2, t1, t2, _ = st.session_state["params"]

        st.markdown("""
### Governing Equations (Lagrangian Mechanics)

The system is described by four coupled nonlinear ODEs:

- θ̇₁ = ω₁  
- θ̇₂ = ω₂  

Angular accelerations depend on gravity, geometry and coupling
between the pendulums.

### Numerical Method
- Adaptive Runge–Kutta (RK45)
- Relative tolerance: 1e-9
- Absolute tolerance: 1e-9
""")

        st.subheader("Initial State Vector")
        st.code(f"[θ₁, ω₁, θ₂, ω₂] = [{t1:.3f}, 0.0, {t2:.3f}, 0.0]")

        st.subheader("Live Parameter Values")
        st.write({
            "Mass 1 (kg)": m1,
            "Mass 2 (kg)": m2,
            "Length 1 (m)": L1,
            "Length 2 (m)": L2,
            "Gravity (m/s²)": 9.81
        })

# ================= RESULTS ================= #
elif section == "Results & Plots":
    st.title("📊 Results & Analysis")

    if "data" not in st.session_state:
        st.warning("Run the simulation first.")
    else:
        d = st.session_state["data"]

        col1, col2 = st.columns(2)

        with col1:
            st.pyplot(trajectory(d["x2"], d["y2"]))
            st.pyplot(phase_space(d["theta1"], d["omega1"], "Pendulum 1"))

        with col2:
            st.pyplot(angle_time(d["t"], d["theta1"], d["theta2"]))
            st.pyplot(phase_space(d["theta2"], d["omega2"], "Pendulum 2"))

        st.pyplot(energy_plot(d["t"], d["energy"]))

        st.subheader("Numerical Summary")
        st.write({
            "Max θ₁ (rad)": float(np.max(d["theta1"])),
            "Max θ₂ (rad)": float(np.max(d["theta2"])),
            "Mean Energy (J)": float(np.mean(d["energy"])),
            "Energy Std Dev": float(np.std(d["energy"]))
        })
