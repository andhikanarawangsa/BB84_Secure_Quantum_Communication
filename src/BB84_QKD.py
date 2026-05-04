# Quantum Key Distribution (BB84) Protocol Simulation
# Authors:
# - Andhika Narawangsa Susilo
# - Muhammad Zaky Hermawan
# - Fairuz Apuilla Rahagi

# Description
# This project simulates a Quantum Key Distribution (BB84) protocol
# combined with post-quantum symmetric encryption (AES-GCM).

import os
import argparse
import random

from sys import argv
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# -------------------- QUANTUM UTIL --------------------
# Extracts measurement results from a quantum circuit simulation.
# Qiskit returns results in little-endian format, so reversal is required.
def get_measurement_result(circuit):
    simulator = AerSimulator()
    circ = transpile(circuit, simulator)
    result = simulator.run(circ, shots=1, memory=True).result()
    memory = result.get_memory(circ)
    return list(reversed(memory[0]))

# Generates truly random classical bits using quantum superposition.
# This serves as a quantum-based randomness source for BB84 protocol.
def quantum_random_number_generator(num_bits):
    circ = QuantumCircuit(1, 1)
    circ.h(0)
    circ.measure(0, 0)

    simulator = AerSimulator()
    circ = transpile(circ, simulator)
    result = simulator.run(circ, shots=num_bits, memory=True).result()
    memory = result.get_memory(circ)

    return list(reversed(memory))

# -------------------- ENCODING --------------------
# Encodes classical bits into quantum states using BB84 encoding rules.
# Rectilinear basis: |0⟩, |1⟩
# Diagonal basis: |+⟩, |-⟩
def encode_qubits(num_bits, random_bits, bases):
    qc = QuantumCircuit(num_bits, num_bits)

    for i in range(num_bits):
        if bases[i] == '0':  # rectilinear
            if random_bits[i] == '1':
                qc.x(i)
        else:  # diagonal
            if random_bits[i] == '0':
                qc.h(i)
            else:
                qc.x(i)
                qc.h(i)

    qc.barrier()
    return qc

# -------------------- EVE --------------------
# Simulates intercept-resend attack by an eavesdropper (Eve).
# Eve measures qubits in random bases and resends collapsed states.
# This introduces disturbance detectable via QBER.
def eavesdrop_qubits(qc, eve_bases):
    for i in range(qc.num_qubits):
        if eve_bases[i] == '1':
            qc.h(i)

    qc.measure(range(qc.num_qubits), range(qc.num_qubits))
    results = get_measurement_result(qc)

    # Reset is used to simulate re-preparation of qubits after Eve's interception
    qc.reset(range(qc.num_qubits))

    for i in range(qc.num_qubits):
        if results[i] == '1':
            qc.x(i)
        if eve_bases[i] == '1':
            qc.h(i)

    qc.barrier()
    return qc

# -------------------- BOB MEASURE --------------------
# Bob measures received qubits using his randomly chosen bases.
# Matching basis yields correct bit recovery (BB84 sifting principle).
def measure_qubits(qc, bases):
    for i in range(qc.num_qubits):
        if bases[i] == '1':
            qc.h(i)

    qc.measure(range(qc.num_qubits), range(qc.num_qubits))
    results = get_measurement_result(qc)

    qc.barrier()
    return qc, results


# -------------------- KEY FUNCTIONS --------------------
# Determines which Alice and Bob bases match for key sifting.
def get_correct_bases(a, b):
    return [a[i] == b[i] for i in range(len(a))]

# Extracts shared secret key bits where Alice and Bob used identical bases.
def sift(correct, data):
    return [data[i] for i in range(len(correct)) if correct[i]]

# Derives a cryptographically secure symmetric key using HKDF-SHA256.
# This ensures quantum-derived bits are transformed into AES-256 key material.
def derive_key(secret, salt, info):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=info,
    )
    return hkdf.derive(secret)

# -------------------- SIMULATION FUNCTION --------------------
def run_bb84_once(num_bits=32, eve_enabled=True):
    random_bits = quantum_random_number_generator(num_bits)
    alice_bases = quantum_random_number_generator(num_bits)
    bob_bases = quantum_random_number_generator(num_bits)

    qc = encode_qubits(num_bits, random_bits, alice_bases)

    if eve_enabled:
        eve_bases = quantum_random_number_generator(num_bits)
        qc = eavesdrop_qubits(qc, eve_bases)

    qc, bob_results = measure_qubits(qc, bob_bases)

    correct_bases = get_correct_bases(alice_bases, bob_bases)

    alice_key = sift(correct_bases, random_bits)
    bob_key = sift(correct_bases, bob_results)

    # ---- QBER ----
    QBER_THRESHOLD = 0.11

    valid_indices = [i for i in range(len(correct_bases)) if correct_bases[i]]
    if len(valid_indices) == 0:
        return {"qber": 0, "detected": False, "keys_match": False}

    sample_size = max(1, len(valid_indices) // 4)
    sample = random.sample(valid_indices, min(sample_size, len(valid_indices)))

    errors = sum(1 for i in sample if random_bits[i] != bob_results[i])
    tested = len(sample)

    qber = errors / tested if tested > 0 else 0
    detected = qber > QBER_THRESHOLD

    # ---- key match ----
    if len(alice_key) == 0 or len(bob_key) == 0:
        return {"qber": qber, "detected": detected, "keys_match": False}

    salt = os.urandom(16)
    info = b"shared_secret_key"

    alice_derived = derive_key(bytes(int(b) for b in alice_key), salt, info)
    bob_derived = derive_key(bytes(int(b) for b in bob_key), salt, info)

    keys_match = alice_derived == bob_derived

    return {
        "qber": qber,
        "detected": detected,
        "keys_match": keys_match
    }

# -------------------- MAIN --------------------
# Main pipeline executing BB84 quantum key distribution simulation,
# including optional eavesdropping scenario and AES-GCM encryption demo.
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("num_bits", type=int, help="Number of qubits/bits")
    parser.add_argument("--eavesdrop", type=int, default=0, help="0 = no Eve, 1 = Eve active")

    args = parser.parse_args()

    num_bits = args.num_bits
    eve_enabled = args.eavesdrop == 1

    random_bits = quantum_random_number_generator(num_bits)
    alice_bases = quantum_random_number_generator(num_bits)
    bob_bases = quantum_random_number_generator(num_bits)

    qc = encode_qubits(num_bits, random_bits, alice_bases)

    eve_used = False
    if eve_enabled:
        eve_used = True
        eve_bases = quantum_random_number_generator(num_bits)
        qc = eavesdrop_qubits(qc, eve_bases)

    qc, bob_results = measure_qubits(qc, bob_bases)
    
    print("\n===== QUANTUM CIRCUIT =====")
    print(qc.draw())

    print("\n===== BIT COMPARISON =====")
    print(f"{'Qubit':<8}{'Alice (orig)':<15}{'Bob (recv)':<15}{'Match':<10}")
    print("-" * 50)

    for i in range(num_bits):
        match = "True" if random_bits[i] == bob_results[i] else "False"
        print(f"{i:<8}{random_bits[i]:<15}{bob_results[i]:<15}{match:<10}")

    correct_bases = get_correct_bases(alice_bases, bob_bases)
    
    print("Matching basis ratio:", sum(correct_bases) / len(correct_bases))

    alice_key = sift(correct_bases, random_bits)
    bob_key = sift(correct_bases, bob_results)

    # ---- detection test (QBER sample) ----
    # Quantum Bit Error Rate (QBER) estimation used to detect channel disturbance.
    # A non-zero QBER may indicate presence of an eavesdropper.
    QBER_THRESHOLD = 0.11

    sample_size = max(1, len(correct_bases) // 4)
    sample = random.sample(range(len(correct_bases)), sample_size)

    errors = 0
    tested = 0

    for i in sample:
        if correct_bases[i]:
            tested += 1
            if random_bits[i] != bob_results[i]:
                errors += 1

    qber = errors / tested if tested > 0 else 0
    detected = qber > QBER_THRESHOLD

    # ---- CASE 2: Eve detected ----
    if eve_enabled and detected:
        print("Detection bit altered: Eavesdropper detected! Aborting key generation")
        return

    # ---- key derivation ----
    if len(alice_key) == 0 or len(bob_key) == 0:
        print("Key generation failed")
        return

    salt = os.urandom(16)
    info = b"shared_secret_key"

    alice_derived = derive_key(bytes(int(b) for b in alice_key), salt, info)
    bob_derived = derive_key(bytes(int(b) for b in bob_key), salt, info)

    keys_match = alice_derived == bob_derived

    print("Alice key == Bob key:", keys_match)

    # ---- CASE 3: mismatch without detection ----
    if eve_enabled and not detected and not keys_match:
        print("Decryption failed, potential eavesdropper but undetected!")
        return

    # ---- encryption ----
    # Demonstrates classical symmetric encryption using quantum-generated keys.
    # AES-GCM ensures confidentiality and integrity of the shared message.
    msg = b"Secret Message"
    nonce = os.urandom(12)

    aes_a = AESGCM(alice_derived)
    ct = aes_a.encrypt(nonce, msg, None)

    aes_b = AESGCM(bob_derived)

    pt = aes_b.decrypt(nonce, ct, None)

    print("Ciphertext:", ct.hex())
    print("Decrypted message:", pt.decode())

    # ---- CASE 4 warning ----
    # Security edge case: Eve is present but remains undetected due to sampling limitations.
    # Highlights probabilistic nature of eavesdropper detection in BB84.
    if eve_enabled and not detected and keys_match:
        print("WARNING: Eve exists but no bits were altered!")


if __name__ == "__main__":
    main()