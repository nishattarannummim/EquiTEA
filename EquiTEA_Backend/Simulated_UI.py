"""
Simulated_UI.py

This script provides a lightweight interactive interface for testing and
demonstrating the EquiTEA backend wage-processing workflow.

The interface allows an operator to manually input a worker ID and collected
weight, then submit the data to the backend API. The backend subsequently
interacts with the blockchain smart contract and returns transaction metadata.

This module is intended strictly for simulation, validation, and research
demonstration purposes.
"""
import streamlit as st
import requests

st.set_page_config(page_title="EquiTEA Worker Dashboard", layout="wide")

st.title("💼 EquiTEA Worker Dashboard")

# ----------------------------
# Worker input
# ----------------------------
worker_id = st.text_input("Worker ID")
weight = st.number_input("Weight (kg)", min_value=0.0, value=5.0, step=0.1)

# ----------------------------
# Send data button
# ----------------------------
if st.button("Process Wage"):
    with st.spinner("Processing wage on blockchain..."):
        try:
            response = requests.post(
                "http://127.0.0.1:5000/process_wage_direct",  # Use Flask backend
                json={"worker_id": worker_id, "weight": weight}
            )
            result = response.json()

            if result.get("status") == "success":
                st.success(f"✅ Wage processed for {result['worker_id']}")
                
                # Display transaction details
                st.subheader("Blockchain Transaction Details")
                st.write(f"**Transaction Hash:** {result['tx_hash']}")
                st.write(f"**Block Number:** {result['blockNumber']}")
                st.write(f"**Gas Used:** {result['gasUsed']}")
                st.write(f"**Weight Processed:** {result['weight_kg']} kg")

            else:
                st.error(f"❌ Error: {result.get('message')}")
        
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to the backend. Make sure Flask server is running.")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
