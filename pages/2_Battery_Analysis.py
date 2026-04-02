import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from scipy.io import loadmat

st.set_page_config(page_title="Battery Analysis", page_icon="🔋", layout="wide")

st.title("Battery Data & Health Analysis")
st.markdown("Analyze battery charging/discharging behavior and internal health indicators.")

tab1, tab2 = st.tabs(["Telemetry Data (CSV)", "NASA Battery Health (MAT)"])

with tab1:
    st.header("Battery Log Telemetry")
    
    @st.cache_data
    def load_csv_data(filepath):
        if os.path.exists(filepath):
            return pd.read_csv(filepath)
        return None

    csv_path = "battery_log.csv"
    csv_data = load_csv_data(csv_path)
    
    if csv_data is not None:
        csv_data['Power_Watts'] = csv_data['Voltage'] * csv_data['Current']
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.subheader("Settings")
            overheat_threshold = st.slider("Overheating Threshold (°C)", 30, 60, 45)
            
            total_energy = csv_data['Power_Watts'].sum()
            max_power = csv_data['Power_Watts'].max()
            avg_temp = csv_data['Temperature'].mean()
            
            st.metric("Total Energy Consumed", f"{total_energy:.2f} Ws")
            st.metric("Max Power", f"{max_power:.2f} W")
            st.metric("Avg Temperature", f"{avg_temp:.2f} °C")
            
        with col2:
            st.subheader("Time vs Temperature")
            overheating = csv_data[csv_data['Temperature'] > overheat_threshold]
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=csv_data['Time'], y=csv_data['Temperature'], mode='lines', name='Temperature (°C)', line=dict(color='orange')))
            fig1.add_trace(go.Scatter(x=overheating['Time'], y=overheating['Temperature'], mode='markers', name='Overheating', marker=dict(color='red', size=8)))
            fig1.add_hline(y=overheat_threshold, line_dash="dash", line_color="red", annotation_text='Threshold')
            fig1.update_layout(title='Time vs Temperature', xaxis_title='Time (s)', yaxis_title='Temperature (°C)')
            st.plotly_chart(fig1, use_container_width=True, config={'doubleClickDelay': 500})
            
            st.subheader("Time vs Voltage & Power")
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=csv_data['Time'], y=csv_data['Voltage'], mode='lines', name='Voltage (V)', line=dict(color='blue')))
            fig2.add_trace(go.Scatter(x=csv_data['Time'], y=csv_data['Power_Watts'], mode='lines', name='Power (W)', line=dict(color='green')))
            fig2.update_layout(title='Time vs Voltage & Power', xaxis_title='Time (s)', yaxis_title='V / W')
            st.plotly_chart(fig2, use_container_width=True, config={'doubleClickDelay': 500})
    else:
        st.warning(f"Could not find {csv_path} in the project directory.")

with tab2:
    st.header("NASA Battery Dataset Extraction")
    
    # Dynamically find .mat files
    mat_files = [f for f in os.listdir('.') if f.endswith('.mat')]
    
    if mat_files:
        selected_mat = st.selectbox("Select NASA Dataset", mat_files)
        
        @st.cache_data
        def load_nasa_data(filepath):
            try:
                mat_data = loadmat(filepath)
                # Ensure the root key matches the filename (e.g. B0005)
                key = filepath.split('.')[0]
                raw_data = mat_data[key]
                cycles = raw_data[0, 0]['cycle']
                
                # Identify simple discharge indices
                discharge_indices = []
                for i in range(len(cycles[0])):
                    if cycles[0, i]['type'][0] == 'discharge':
                        discharge_indices.append(i)
                return cycles, discharge_indices
            except Exception as e:
                return None, None
                
        cycles, discharge_indices = load_nasa_data(selected_mat)
        
        if cycles is not None and discharge_indices:
            st.success(f"Loaded {len(discharge_indices)} discharge cycles from {selected_mat}.")
            
            selected_cycle_idx = st.selectbox("Select Discharge Cycle Index", range(len(discharge_indices)))
            actual_cycle = discharge_indices[selected_cycle_idx]
            
            cycle_data = cycles[0, actual_cycle]
            measurements = cycle_data['data'][0, 0]
            
            voltage = measurements['Voltage_measured'].flatten()
            time_sec = measurements['Time'].flatten()
            
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=time_sec, y=voltage, mode='lines', name='Measured Voltage', line=dict(color='blue')))
            fig3.add_hline(y=4.2, line_dash="dot", line_color="green", annotation_text='Nominal Max (4.2V)')
            fig3.add_hline(y=3.0, line_dash="dot", line_color="red", annotation_text='Cut-off (3.0V)')
            fig3.update_layout(title=f"Discharge Profile: Cycle {actual_cycle}", xaxis_title="Time (s)", yaxis_title="Voltage (V)")
            st.plotly_chart(fig3, use_container_width=True, config={'doubleClickDelay': 500})
        else:
            st.error(f"Failed to extract discharge cycles from {selected_mat}.")
    else:
        st.warning("No .mat files found in the project root directory. Please add NASA Battery datasets.")
