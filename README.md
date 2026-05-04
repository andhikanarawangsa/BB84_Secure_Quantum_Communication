# Quantum Key Distribution (BB84) Simulation with Qiskit and AES-GCM
## Overview
This project implements a simulation of the **BB84 Quantum Key Distribution (QKD) protocol** using Qiskit, combined with classical post-quantum symmetric encryption using **AES-GCM**.
The system demonstrates how quantum mechanics can be used to establish a secure shared key between two parties (Alice and Bob), and how an eavesdropper (Eve) affects the communication channel.

---

## Key Features
- BB84 quantum key distribution simulation using Qiskit Aer
- Random quantum basis selection (rectilinear and diagonal)
- Optional intercept-resend eavesdropping attack simulation
- Quantum Bit Error Rate (QBER) estimation for eavesdropper detection
- Key reconciliation (basis sifting)
- Key derivation using HKDF-SHA256
- Symmetric encryption using AES-GCM
- Circuit visualization using Qiskit `QuantumCircuit.draw()`
- Detailed bit-level comparison between Alice and Bob

---

## System Architecture
The simulation consists of four main stages:

1. **Quantum State Preparation (Alice)**
   - Random bit generation
   - Random basis selection
   - Qubit encoding

2. **Quantum Channel (Optional Eve)**
   - Intercept-resend attack simulation
   - Measurement and re-preparation of qubits

3. **Measurement (Bob)**
   - Random basis selection
   - Qubit measurement and result extraction

4. **Classical Post-Processing**
   - Basis reconciliation (sifting)
   - QBER estimation
   - Key derivation using HKDF
   - AES-GCM encryption/decryption

---

## Eavesdropping Model
The eavesdropper (Eve) performs an **intercept-resend attack**, where:
- Qubits are measured using random bases
- Quantum states collapse due to measurement
- Resent qubits introduce detectable disturbances
Detection is performed using a simplified **Quantum Bit Error Rate (QBER)** estimation.

---

## Installation
```bash
pip install -r requirements.txt
```

---
## Usage
Run without eavesdropper
```bash
python qkd.py 20 --eavesdrop 0
```
Run with eavesdropper
```bash
python qkd.py 20 --eavesdrop 1
```
Where:
- 20 = number of qubits/bits
- --eavesdrop: 0 (no Eve) / 1 (Eve Active)

---
## Example Output
### Quantum Circuit
(Quantum circuit diagram rendered by Qiskit)

### Bit Comparison Table
Qubit   Alice (orig)   Bob (recv)     Match
--------------------------------------------------
0       0              0              True
1       1              0              False
...

### Key Result
Alice key == Bob key: True
Ciphertext: <hex output>
Decrypted message: Secret Message

### Matching Basis Ratio
The matching basis ratio typically fluctuates between: `0.45 – 0.65`
This aligns with the theoretical probability of basis agreement in BB84: `P(match) = 0.5`
Finite sample size introduces statistical variation.

## Security Analysis
- Without eavesdropping, Alice and Bob derive identical keys.
- With eavesdropping, QBER increases due to quantum state disturbance.
- Undetected eavesdropping is possible in limited sampling scenarios, highlighting the probabilistic nature of BB84 security.

## Requirements
see `requirements.txt`