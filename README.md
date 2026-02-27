# Applied Python for Electrical Engineering & EV Systems

**Objective:** A computational laboratory for simulating, analyzing, and optimizing Battery Management Systems (BMS) using Python.

## 📂 Repository Contents

### 1. Battery Logic & Control
*   Fundamental EV calculations (Watt-hour capacity, C-rate).
*   Charging control loops (CC/CV simulation).
*   Basic circuit modeling.

### 2. Signal Processing & Simulation
*   Synthetic sensor data generation with Gaussian noise injection.
*   Fault detection algorithms (Over-current logic).
*   Li-ion discharge curve modeling with UVLO (Under-Voltage Lockout).

### 3. Real-World Data Analytics
**A. Sensor Log Diagnostics (Pandas)**
*   Ingestion of time-series CSV sensor logs (Voltage, Current, Temp).
*   Thermal event detection filters (e.g., T > 30°C) to identify safety risks.
*   Calculated derived physics metrics: Instantaneous **Power (W)** and **Total Energy (Wh)**.

**B. NASA PCoE Battery Research (Advanced)**
*   **MATLAB Bridge:** Built a custom parser using `scipy.io` to mine data from nested NASA `.mat` structs.
*   **SOH Estimator:** Algorithmically extracted specific discharge cycles and implemented **numerical integration (Trapezoidal Rule)** to calculate Total Capacity (Ah).
*   **Degradation Analysis:** Visualized voltage relaxation effects and capacity fade compared to rated specifications (SOH%).
*   **Dashboard:** 3-View subplot visualizing synchronized V/I/T thermodynamic profiles.
*   **Lifecycle Aging Analysis:** Generated the complete **Capacity Degradation Curve** across 168 cycles, successfully identifying the **End-of-Life (EOL)** point and characterizing **Capacity Regeneration** phenomena during rest periods.

### 4. Predictive Maintenance (Scalability & Machine Learning)
*   **Automated Batch Processing:** Created Python functions to dynamically parse and aggregate data from multiple battery datasets simultaneously.
*   **Comparative Analysis:** Analyzed performance variance across different physical cells to identify "Strong" vs "Weak" batteries.
*   **Remaining Useful Life (RUL) Prediction:** Integrated linear regression algorithms to forecast the precise cycle number where battery health will cross the critical 70% threshold.
*   
## 🛠 Tools Used
*   **Language:** Python 3.12+
*   **Libraries:** NumPy, Pandas, Matplotlib, SciPy
*   **Environment:** Jupyter Notebook / Anaconda

---
**Author:** Ohi
**Status:** Active Development

## 📚 Dataset Reference
*   **Source:** [NASA Prognostics Data Repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/)
*   **Dataset:** "6. Li-ion Battery Aging Datasets"
*   **Citation:** B. Saha and K. Goebel (2007). "Battery Data Set", NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA.
