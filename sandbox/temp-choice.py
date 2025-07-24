from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit_aer.noise import thermal_relaxation_error, NoiseModel
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Generate thermal noise model for a given T1, T2, and gate time
def create_thermal_noise_model(T1, T2, gate_time=100e-9):
    error = thermal_relaxation_error(T1, T2, gate_time)
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error, ['id', 'u1', 'u2', 'u3', 'x', 'h'])
    return noise_model

# Circuit to create equal superposition over 3 qubits => 8 outcomes
def create_random_choice_circuit():
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.barrier()
    qc.id(0)  # simulate time passing for T1/T2 decay
    qc.id(1)
    qc.id(2)
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc

# T1/T2 settings for different "temperatures"
settings = {
    "Low Temp (T1=100μs)": (100e-6, 80e-6),
    "Medium Temp (T1=20μs)": (20e-6, 16e-6),
    "High Temp (T1=5μs)": (5e-6, 4e-6)
}

backend = Aer.get_backend("qasm_simulator")
shots = 10000
results = []
labels = []

# Run simulation for each temperature setting
for label, (T1, T2) in settings.items():
    noise_model = create_thermal_noise_model(T1, T2)
    qc = create_random_choice_circuit()
    tqc = transpile(qc, backend)
    job = backend.run(tqc, noise_model=noise_model, shots=shots)
    result = job.result()
    counts = result.get_counts()
    results.append(dict(counts))
    labels.append(label)

# Plot results
plot_histogram(results, legend=labels, title="Effect of T1/T2 Decay on 3-Qubit Random Choice")
plt.show()
