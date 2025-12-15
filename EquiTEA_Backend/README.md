# EquiTEA Backend

This folder contains the **computer-based backend implementation** of the EquiTEA system.

In this version, **face recognition and decision logic are executed on a laptop or PC** using Python libraries. The backend server handles worker identification, assigns work output, and triggers blockchain wage transactions.

This backend was developed as the **initial prototype** to validate the end-to-end system before the integration of IoT hardware.

---

## Role of This Backend

- Run face recognition using Python on a computer
- Identify workers using stored facial images
- Assign or simulate collected weight
- Interact with the blockchain smart contract
- Process wage payments automatically
- Provide a simulation interface for testing (`Simulated_UI.py`)

---

## System Flow (Backend Version)

1. A facial image is sent to the backend server.
2. The backend:
   - Extracts face embeddings using the `face_recognition` Python library.
   - Matches the face against stored worker images.
3. If a match is found:
   - A worker ID is retrieved.
   - A **static weight value** is assigned (prototype stage).
4. The backend calls the blockchain smart contract.
5. A wage transaction is recorded on-chain.
6. Optionally, the simulation interface (`Simulated_UI.py`) allows manual wage processing for demonstration purposes.

---

## Files

### `app.py`

- Flask-based backend server
- Loads known worker face images from `known_faces/` and generates embeddings
- Performs face recognition using CPU
- Calls blockchain wage processing upon successful recognition
- Contains an additional endpoint `/process_wage_direct` for **direct wage processing**
- Static weight values are used for prototype demonstration

---

### `blockchain.py`

- Manages all blockchain-related operations
- Connects to an Ethereum test network (Sepolia)
- Interacts with the deployed smart contract (`EquiTEA.sol`)
- Supports:
  - Worker registration
  - Wage rate configuration
  - Wage payment processing
- Implements nonce management to avoid transaction conflicts
- Sensitive information (private keys, RPC URLs, wallet addresses) is **excluded** from the public repository

---

### `test_request.py`

- Standalone Python script for testing blockchain operations
- Registers a worker, sets a wage rate, and triggers wage payments manually
- Helps validate blockchain logic **independently of face recognition**

---

### `Simulated_UI.py`

- Interactive simulation interface for wage processing
- Inputs:
  - Worker ID
  - Weight (kg)
- Sends HTTP requests to the backend endpoint `/process_wage_direct`
- Displays blockchain transaction details:
  - Transaction hash
  - Block number
  - Gas used
  - Weight processed
- Designed for demonstration and controlled testing, not real-time deployment

---

### `known_faces/`

- Stores facial images of registered workers
- Organized by worker ID subfolders
- Used only to generate facial embeddings at runtime
- **No real facial images are included** in the public repository

---

## Notes and Limitations

- Face recognition is performed on a **computer**, not an IoT device
- Static weight values are used in place of real sensors
- Designed for prototype and research validation
- Security, scalability, and production deployment are **out of scope**

---

## Purpose

This backend serves as the **baseline implementation** of EquiTEA. It demonstrates worker identification, wage calculation, and blockchain integration. The architecture was later extended with IoT-based face recognition using **ESP32 and Edge Impulse** for field deployment.
