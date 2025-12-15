# EquiTEA IoT Module

This folder contains the IoT-side implementation of the EquiTEA system, built around an ESP32 device and Edge Impulse.

The IoT module is responsible for worker identification and data transmission.

---

## Responsibilities

- Capture worker images using ESP32 camera
- Run on-device face recognition model
- Identify registered workers
- Send worker ID to backend server

---

## Files

### `main_code.ino`

- Primary ESP32 firmware
- Integrates:
  - Camera input
  - Edge Impulse inference
  - Network communication
- Sends recognized worker ID to backend

---

### `sketch_oct22a.ino`

- Initial testing and setup code
- Used for ESP32 configuration and camera validation

---

### `app_esp32.py`

- Supporting Python script used during development
- Assisted in testing communication and logic flow

---

### `blockchain.py`

- Lightweight blockchain-related logic
- Used for testing and early-stage integration
- Not intended for direct on-device blockchain execution

---

### `EquiTEA_Image_Classification_inferencing/`

- Edge Impulse generated inference code
- Implements image classification-based face recognition
- Operates in **closed-set mode**
  - Only recognizes workers included during training
  - Unknown faces are rejected

---

## Model Characteristics

- Image classification (not open-set recognition)
- Optimized for low-power embedded device
- Suitable for fixed workforce environments

---

## Notes

- The IoT module does not store personal data
- Face recognition is limited to trained identities
- Designed for prototype and research use
