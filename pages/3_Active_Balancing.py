import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Active Balancing", page_icon="⚖️", layout="wide")

st.title("Active Battery Cell Balancing")
st.markdown("Simulate an active balancing circuit behavior across multiple battery cells.")

st.sidebar.header("Initial Cell Voltages")
cell1 = st.sidebar.number_input("Cell 1 (V)", min_value=2.5, max_value=4.2, value=4.1, step=0.01)
cell2 = st.sidebar.number_input("Cell 2 (V)", min_value=2.5, max_value=4.2, value=3.8, step=0.01)
cell3 = st.sidebar.number_input("Cell 3 (V)", min_value=2.5, max_value=4.2, value=3.5, step=0.01)
cell4 = st.sidebar.number_input("Cell 4 (V)", min_value=2.5, max_value=4.2, value=4.0, step=0.01)

st.sidebar.header("Simulation Settings")
imbalance_threshold = st.sidebar.slider("Imbalance Threshold (V)", 0.01, 0.20, 0.05, 0.01)
balance_step = st.sidebar.slider("Balancing Step Size (V)", 0.01, 0.10, 0.02, 0.01)
max_iterations = st.sidebar.slider("Max Iterations", 10, 200, 50, 1)

if st.button("Run Active Balancing Simulation", type="primary"):
    cells = np.array([cell1, cell2, cell3, cell4], dtype=float)
    
    history = [cells.copy()]
    
    iteration = 0
    balanced = False
    
    while not balanced and iteration < max_iterations:
        max_idx = np.argmax(cells)
        min_idx = np.argmin(cells)
        
        diff = cells[max_idx] - cells[min_idx]
        
        if diff <= imbalance_threshold:
            balanced = True
        else:
            cells[max_idx] -= balance_step
            cells[min_idx] += balance_step
            history.append(cells.copy())
            iteration += 1
            
    # Visualize
    history = np.array(history)
    
    st.subheader(f"Balancing Results (Converged: {balanced})")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        fig = go.Figure()
        for i in range(4):
            fig.add_trace(go.Scatter(x=list(range(len(history))), y=history[:, i], mode='lines+markers', name=f'Cell {i+1}'))
            
        fig.update_layout(title="Cell Voltages over Balancing Iterations",
                          xaxis_title="Iteration",
                          yaxis_title="Voltage (V)")
        st.plotly_chart(fig, use_container_width=True, config={'doubleClickDelay': 500})
        
    with col2:
        st.metric("Total Iterations", iteration)
        st.metric("Final Max Diff", f"{(np.max(cells) - np.min(cells)):.3f} V")
        
        st.write("### Final Voltages")
        st.write(f"Cell 1: {cells[0]:.2f} V")
        st.write(f"Cell 2: {cells[1]:.2f} V")
        st.write(f"Cell 3: {cells[2]:.2f} V")
        st.write(f"Cell 4: {cells[3]:.2f} V")
