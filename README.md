# Quantum Key Distribution (BB84) Simulation with Qiskit and AES-GCM

![Language](https://img.shields.io/badge/Language-Python-blue)
![Qiskit](https://img.shields.io/badge/Qiskit-Quantum-purple)
![Quantum](https://img.shields.io/badge/Quantum-BB84-blueviolet)
![Cryptography](https://img.shields.io/badge/Cryptography-AES--256_GCM-green)
![HKDF](https://img.shields.io/badge/KDF-HKDF--SHA256-orange)
![Simulator](https://img.shields.io/badge/Backend-Qiskit_Aer-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

📄 **Technical Report:** [QKD_BB84_Report.pdf](report/QKD_BB84_Report.pdf)

This project implements a simulation of the **BB84 Quantum Key Distribution (QKD) protocol** using Qiskit, combined with classical post-quantum symmetric encryption using **AES-GCM**.

---

## Key Features
- BB84 quantum key distribution protocol simulation using Qiskit Aer
- Quantum-based random bit and basis generation
- Support for both rectilinear and diagonal encoding bases
- Optional intercept-resend eavesdropping attack model
- Quantum Bit Error Rate (QBER) estimation for eavesdropper detection
- Basis reconciliation (key sifting) for shared key extraction
- Key derivation using HKDF-SHA256 (AES-256 compatible)
- Symmetric encryption using AES-GCM for secure message exchange
- Quantum circuit visualization using Qiskit `QuantumCircuit.draw()`
- Bit-level comparison between Alice and Bob measurement outcomes
- Statistical experiment mode for evaluating detection rate and QBER convergence

---

## Limitations
- This implementation uses a simulated quantum environment (Qiskit Aer), not a physical quantum channel.
- Noise models are not included, resulting in near-ideal channel conditions.
- Eavesdropper detection is based on simplified QBER sampling, not full protocol security proofs.

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
The project supports two modes: a single-run demonstration and a multi-run statistical experiment.

### 1. Single Run (Protocol Demonstration)
Run a single BB84 simulation to observe the full protocol flow:

Run without eavesdropper
```bash
python qkd.py 20 --eavesdrop 0
```
Run with eavesdropper
```bash
python qkd.py 20 --eavesdrop 1
```
This mode provides detailed output including:
- Circuit visualization using Qiskit `QuantumCircuit.draw()`
- Bit-by-bit comparison between Alice and Bob
- Matching basis ratio
- Derived keys (Alice vs Bob)
- AES-GCM encryption and decryption results

### 2. Multiple Runs (Statistical Experiment)
Run repeated simulations to evaluate protocol performance:
```bash
python simulation.py 20 --runs 100 --eavesdrop 1
```
This mode provides statistical metrics:
- Average Quantum Bit Error Rate (QBER)
- Eavesdropper detection rate
- Key mismatch rate
- Detection rate convergence graph

#### Parameters
- 20 = number of qubits/bits
- --eavesdrop: 0 (no Eve) / 1 (Eve Active)
- --runs (experiment mode only): Number of repeated simulations

---
## Example Output
### Quantum Circuit
(Quantum circuit diagram rendered by Qiskit)

### Bit Comparison Table
| Qubit | Alice (orig) | Bob (recv) | Match |
|------:|--------------:|------------:|:------:|
| 0     | 0             | 0           | True   |
| 1     | 1             | 0           | False  |
...

### Key Result
Alice key == Bob key: True

Ciphertext: <hexadecimal output>

Decrypted message: Secret Message

### Matching Basis Ratio
The matching basis ratio typically fluctuates between: `0.45 – 0.65`.
This aligns with the theoretical probability of basis agreement in BB84: `P(match) = 0.5`.
Finite sample size introduces statistical variation.

## Security Analysis
- Without eavesdropping, Alice and Bob derive identical keys.
- With eavesdropping, QBER increases due to quantum state disturbance.
- Undetected eavesdropping is possible in limited sampling scenarios, highlighting the probabilistic nature of BB84 security.

## Requirements
See `requirements.txt` for the full list of dependencies.

## Technologies Used
- Qiskit (Quantum Simulation)
- Qiskit Aer (Quantum backend simulator)
- Cryptography (HKDF, AES-GCM)
- Python 3.10+

## Authors

- Andhika Narawangsa Susilo
- Muhammad Zaky Hermawan
- Fairuz Apuilla Rahagi

---

## Academic Integrity Notice

This project is published as part of an academic portfolio.
Unauthorized reuse or plagiarism of this work is discouraged.

*Note: This work was completed prior to publication and is shared
retrospectively for academic portfolio purposes.*

---

## License

This project is released for academic and research purposes only.

*Originally developed: 2025 — Published: 2026*

