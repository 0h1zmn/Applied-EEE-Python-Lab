import streamlit as st
import numpy as np
import plotly.graph_objects as go
import os
from scipy.io import loadmat
from scipy.integrate import trapezoid
from scipy.stats import linregress

st.set_page_config(page_title="Comparative Analysis", page_icon="📊", layout="wide")

st.title("Comparative Battery Degradation Analysis")
st.markdown("Compare the State of Health (SOH) degradation across multiple NASA battery datasets and forecast their expected End of Life (EOL) cycle.")

# Dynamically find .mat files
mat_files = [f for f in os.listdir('.') if f.endswith('.mat')]

if not mat_files:
    st.warning("No .mat files found in the project directory. Please add NASA Battery datasets.")
else:
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.subheader("Analysis Parameters")
        selected_files = st.multiselect("Select Batteries to Compare", mat_files, default=mat_files[:2])
        eol_threshold = st.slider("EOL Threshold (%)", min_value=50, max_value=90, value=70, step=1)
        
    with col2:
        @st.cache_data
        def get_battery_capacity(filepath):
            try:
                mat_data = loadmat(filepath)
                battery_id = filepath.split('.')[0]
                raw_data = mat_data[battery_id]
                cycles = raw_data[0, 0]['cycle']

                discharge_indices = []
                for i in range(len(cycles[0])):
                    if cycles[0][i]['type'][0] == 'discharge':
                        discharge_indices.append(i)
                
                soh_history = []
                for idx in discharge_indices:
                    cycle_data = cycles[0, idx]
                    measurements = cycle_data['data'][0, 0]
                    current = measurements['Current_measured'].flatten()
                    time_sec = measurements['Time'].flatten()
                    capacity = trapezoid(abs(current), time_sec) / 3600
                    rated_capacity = 2.0
                    soh = (capacity / rated_capacity) * 100
                    soh_history.append(soh)
                return soh_history
            except Exception as e:
                return []

        if selected_files:
            fig = go.Figure()
            results = {}
            for f in selected_files:
                soh = get_battery_capacity(f)
                if soh:
                    results[f] = soh
                    fig.add_trace(go.Scatter(x=list(range(len(soh))), y=soh, mode='lines', name=f))
            
            fig.add_hline(y=eol_threshold, line_dash="dash", line_color="red", annotation_text=f"EOL Threshold ({eol_threshold}%)")
            fig.update_layout(title="Comparative Degradation Analysis (NASA Battery Batch)",
                              xaxis_title="Discharge Cycle",
                              yaxis_title="State of Health (%)")
            st.plotly_chart(fig, use_container_width=True, config={'doubleClickDelay': 500})
            
            st.divider()
            st.subheader("Predictive Analytics: End of Life Forecasting")
            
            target_battery = st.selectbox("Select Target Battery for Forecasting", selected_files)
            
            if target_battery in results:
                y = results[target_battery]
                x = np.arange(len(y))
                
                # Perform linear regression
                slope, intercept, r_value, p_value, std_err = linregress(x, y)
                
                current_soh = y[-1]
                
                if slope < 0:
                    predicted_cycle = (eol_threshold - intercept) / slope
                else:
                    predicted_cycle = float('inf') # Degradation is somehow positive (?)
                
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                metric_col1.metric("Degradation Rate", f"{slope:.4f} %/cycle")
                metric_col2.metric("Current State of Health", f"{current_soh:.2f} %")
                
                if predicted_cycle != float('inf') and predicted_cycle > 0:
                    metric_col3.metric("Predicted EOL Cycle", f"Cycle {int(predicted_cycle)}")
                else:
                    metric_col3.metric("Predicted EOL Cycle", "N/A or Already Dead")
                    
                with st.expander("Show Regression Statistics"):
                    st.write(f"R-squared: {r_value**2:.4f}")
                    st.write(f"Standard Error: {std_err:.4f}")
                    st.write(f"Equation: SOH = {slope:.4f} * Cycle + {intercept:.4f}")
                    
        else:
            st.info("Please select at least one battery to begin the analysis.")
