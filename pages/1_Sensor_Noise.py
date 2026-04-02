import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Sensor Noise Simulation", page_icon="📈", layout="wide")

st.title("📈 Sensor Readings & Noise Simulation")

st.markdown("""
This module simulates a Li-ion battery discharge curve and demonstrates how noise affects current sensor readings.
Use the interactive controls below to adjust parameters and observe the effects in real-time.
""")

st.header("Part 1: Li-ion Battery Discharge Curve")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Discharge Parameters")
    discharge_time = st.slider("Discharge Time (seconds)", min_value=100, max_value=2000, value=1000, step=1)
    linear_drop = st.number_input("Linear Drop Factor", value=0.0005, format="%.5f")
    quad_drop = st.number_input("Quadratic Drop Factor", value=0.000001, format="%.6f")
    cut_off = st.slider("Cut-off Voltage (V)", min_value=2.5, max_value=3.5, value=3.0, step=0.01)

with col2:
    time_sec_v = np.linspace(0, discharge_time, 100)
    voltage = 4.2 - (linear_drop * time_sec_v) - (quad_drop * time_sec_v**2)
    voltage = np.clip(voltage, cut_off, 4.2)
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=time_sec_v, y=voltage, mode='lines', name="Voltage"))
    fig1.add_hline(y=cut_off, line_dash="dash", line_color="gray", annotation_text=f"Cut-off Voltage ({cut_off}V)")
    fig1.update_layout(title="Li-ion Battery Discharge Curve",
                       xaxis_title="Time (seconds)",
                       yaxis_title="Voltage (V)")
    st.plotly_chart(fig1, use_container_width=True, config={'doubleClickDelay': 500})

st.divider()

st.header("Part 2: Current Sensor Readings with Noise")

col3, col4 = st.columns([1, 3])

with col3:
    st.subheader("Sensor Parameters")
    sim_time = st.slider("Simulation Time (seconds)", min_value=5, max_value=50, value=10, step=1)
    noise_std = st.slider("Noise Standard Deviation (A)", min_value=0.0, max_value=5.0, value=1.0, step=0.01)
    fault_threshold = st.slider("Fault Threshold (A)", min_value=5.0, max_value=15.0, value=11.0, step=0.1)

with col4:
    time_sec_i = np.linspace(0, sim_time, sim_time * 50)
    # Simulated current with a sinusoidal pattern
    current = 10 * np.sin(time_sec_i)
    noise = np.random.normal(0, noise_std, len(time_sec_i))
    sensor_reading = current + noise

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=time_sec_i, y=sensor_reading, mode='lines', name="Sensor Reading", line=dict(color='blue', width=1), opacity=0.6))
    fig2.add_trace(go.Scatter(x=time_sec_i, y=current, mode='lines', name="True Current", line=dict(color='orange', width=3)))
    fig2.add_hline(y=fault_threshold, line_dash="dot", line_color="red", annotation_text=f"Fault Threshold ({fault_threshold}A)")
    fig2.update_layout(title="Current Sensor Readings with Noise",
                       xaxis_title="Time (seconds)",
                       yaxis_title="Current (A)")
    st.plotly_chart(fig2, use_container_width=True, config={'doubleClickDelay': 500})

    indices = np.where(sensor_reading > fault_threshold)[0]
    fault_times = time_sec_i[indices]
    
    st.warning(f"**Fault Analysis**: {indices.size} readings exceeded the {fault_threshold}A threshold.")
    with st.expander("Show Fault Times (seconds)"):
        st.write(np.round(fault_times, 2))
