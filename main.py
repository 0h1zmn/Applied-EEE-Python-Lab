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
2. **Battery Data Analysis** (Coming Soon):
   - Analyze dataset logs and identify battery degradation patterns.
3. **Active Balancing Logic** (Coming Soon):
   - Explore how different cells in a battery pack balance their voltages over time.

---
**How to run locally:**
```bash
pip install -r requirements.txt
streamlit run main.py
```
""")

# Check for required data files or show a welcoming metric
st.info("👈 Please select a module from the sidebar to begin your interactive simulation.")
