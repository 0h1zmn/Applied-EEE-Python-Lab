import streamlit as st

st.set_page_config(
    page_title="Interactive EEE Dashboard",
    page_icon="🔋",
    layout="wide"
)

st.title("🔋 Interactive EEE Learning Dashboard")

st.markdown("""
Welcome to your interactive Python Electrical and Electronic Engineering (EEE) Journey!

This dashboard consolidates your previous Jupyter Notebook experiments into one unified, interactive place. Use the sidebar to navigate between different simulation and analysis modules:

### 📑 Available Modules:
1. **Sensor Readings & Noise**: 
   - Simulate a Li-ion battery discharge curve.
   - Inject interactive random noise into current sensor readings and track fault times.
2. **Battery Data Analysis**:
   - Analyze CSV telemetry logs (Temperature, Voltage, Power).
   - Extract and interact with NASA `.mat` battery cycle datasets.
3. **Active Balancing Logic**:
   - Explore how different cells in a battery pack balance their voltages interactively over time with Plotly point animations.
4. **Comparative Analysis**:
   - Compare degradation patterns across multiple NASA battery datasets.
   - Run live linear regression to predict End of Life (EOL) cycles based on custom thresholds!
""")

# Check for required data files or show a welcoming metric
st.info("👈 Please select a module from the sidebar to begin your interactive simulation.")
