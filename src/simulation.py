# ==========================================
# Quantum Key Distribution (BB84) Protocol Simulation
# Authors:
# - Andhika Narawangsa Susilo
# - Muhammad Zaky Hermawan
# - Fairuz Apuilla Rahagi
#
# Description:
# This script performs repeated simulations of the BB84 protocol
# to evaluate system performance under multiple runs.
#
# It measures:
# - Quantum Bit Error Rate (QBER)
# - Eavesdropper detection rate
# - Key mismatch rate
#
# The experiment supports optional eavesdropping simulation
# using an intercept-resend attack model.
# ==========================================

import argparse
import matplotlib.pyplot as plt
from BB84_QKD import run_bb84_once


def run_experiment(num_runs, num_bits, eve_enabled):
    # Stores QBER values from each simulation run
    qbers = []

    # Counts how many times an eavesdropper is successfully detected
    detections = 0

    # Counts how often Alice and Bob derive different keys
    mismatches = 0

    # Tracks cumulative detection rate progression for visualization
    detection_progress = []

    # ---------------- MAIN EXPERIMENT LOOP ----------------
    # Repeats BB84 simulation multiple times to obtain statistical metrics
    for i in range(num_runs):
        result = run_bb84_once(num_bits, eve_enabled)

        # Collect QBER (quantum channel disturbance indicator)
        qbers.append(result["qber"])

        # Count detection events based on QBER sampling
        if result["detected"]:
            detections += 1

        # Count key mismatch events (security failure or noise effect)
        if not result["keys_match"]:
            mismatches += 1

        # Compute cumulative detection probability over time
        current_rate = detections / (i + 1)
        detection_progress.append(current_rate)

    # ---------------- STATISTICAL METRICS ----------------
    # Average QBER across all runs (indicates overall channel integrity)
    avg_qber = sum(qbers) / len(qbers)

    # Probability of detecting an eavesdropper
    detection_rate = detections / num_runs

    # Probability that Alice and Bob keys do not match
    mismatch_rate = mismatches / num_runs

    # ---------------- PRINT RESULTS ----------------
    print("\n=== RESULT ===")
    print("Runs:", num_runs)
    print("Bits:", num_bits)
    print("Eve enabled:", eve_enabled)
    print("Average QBER:", avg_qber)
    print("Detection Rate:", detection_rate)
    print("Mismatch Rate:", mismatch_rate)

    # ---------------- VISUALIZATION ----------------
    # Plot how detection rate evolves as the number of runs increases
    # This illustrates convergence behavior in probabilistic detection
    plt.figure()
    plt.plot(range(1, num_runs + 1), detection_progress)
    plt.xlabel("Number of Runs")
    plt.ylabel("Detection Rate")
    plt.title("Detection Rate vs Number of Runs")
    plt.grid()

    # Display the plot
    plt.show()


if __name__ == "__main__":
    # Command-line interface for flexible experiment configuration
    parser = argparse.ArgumentParser()

    parser.add_argument("num_bits", type=int, help="Number of qubits")
    parser.add_argument("--runs", type=int, default=100, help="Number of simulations")
    parser.add_argument("--eavesdrop", type=int, default=1, help="0 = no Eve, 1 = Eve")

    args = parser.parse_args()

    # Execute experiment with given parameters
    run_experiment(
        num_runs=args.runs,
        num_bits=args.num_bits,
        eve_enabled=(args.eavesdrop == 1)
    )