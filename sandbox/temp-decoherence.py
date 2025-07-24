# environmental noise in simulation

# T1: Relaxation Time (Energy Decay)
# Definition: The average time a qubit stays in the excited state |1⟩ before decaying to the ground state |0⟩.\
# Physical meaning: This models energy loss, often due to interaction with the environment (e.g., thermal photons).
# Effect: As time passes, qubits tend to "relax" to |0⟩.
# Higher temperature ⇒ faster decay ⇒ lower T1.

# T2: Dephasing Time (Loss of Coherence)
# Definition: The average time over which a qubit maintains a well-defined phase between |0⟩ and |1⟩ in a superposition.
# Physical meaning: This models how quickly the relative phase between |0⟩ and |1⟩ becomes randomized.
# Effect: Even if the energy state doesn’t change, the superposition (like |+⟩ = (|0⟩ + |1⟩)/√2) loses its quantum interference.
# T2 is always ≤ 2·T1, because it includes relaxation and additional dephasing mechanisms

# When T2 decay happens (as in your earlier temperature simulation), the relative phase gets randomized.
# you get something more like a classical mixture — you still get 50/50 outcomes, but there's no interference anymore.

# That means:
# You can’t use this qubit for interference-based algorithms like Grover’s or Shor’s.
# The quantum behavior is effectively lost — it behaves classically.

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit_aer.noise import thermal_relaxation_error, NoiseModel
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Function to create a noise model for given T1, T2, and gate time
def create_thermal_noise_model(T1, T2, gate_time=100e-9):
    error = thermal_relaxation_error(T1, T2, gate_time)
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error, ['id', 'u1', 'u2', 'u3', 'x', 'h'])
    return noise_model

# Create a simple circuit to test decoherence
def create_test_circuit():
    qc = QuantumCircuit(1, 1)
    qc.h(0)           # Prepare |+> state
    qc.barrier()
    qc.id(0)          # Idle gate (simulate time passing)
    qc.measure(0, 0)
    return qc

# Define different temperature settings (via T1/T2 times)
# Lower T1/T2 corresponds to higher temperature
settings = {
    "Low Temp (T1=100us)": (100e-6, 80e-6),
    "Mid Temp (T1=20us)": (20e-6, 16e-6),
    "High Temp (T1=5us)": (5e-6, 4e-6)
}

backend = Aer.get_backend("qasm_simulator")
shots = 2000#1024
results = []
labels = []

for label, (T1, T2) in settings.items():
    noise_model = create_thermal_noise_model(T1, T2)
    qc = create_test_circuit()
    tqc = transpile(qc, backend)
    job = backend.run(tqc, noise_model=noise_model, shots=shots)
    result = job.result()
    counts = result.get_counts()
    results.append(dict(counts))
    labels.append(label)

# Plot the results
plot_histogram(results, legend=labels, title="Effect of Increasing Temperature via T1/T2 Reduction")
plt.show()
