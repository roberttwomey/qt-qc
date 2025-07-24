from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.quantum_info import DensityMatrix, partial_trace
from qiskit_aer.noise import thermal_relaxation_error, NoiseModel
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Create thermal noise model
def create_thermal_noise_model(T1, T2, gate_time=100e-9):
    error = thermal_relaxation_error(T1, T2, gate_time)
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error, ['id', 'u1', 'u2', 'u3', 'x', 'h'])
    return noise_model

# Step 2: Create a 3-qubit superposition circuit
def create_superposition_circuit():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.barrier()
    qc.id(0)  # simulate idle time
    qc.id(1)
    qc.id(2)
    return qc

# Step 3: Simulate and extract final density matrix
def simulate_density_matrix(qc, noise_model):
    backend = Aer.get_backend('aer_simulator')
    backend.set_options(method='density_matrix')
    qc.save_density_matrix()
    tqc = transpile(qc, backend)
    result = backend.run(tqc, noise_model=noise_model).result()
    final_rho = result.data(0)['density_matrix']
    return DensityMatrix(final_rho)

# Step 4: Visualize real part of density matrix
def plot_density_matrix(dm, title="Density Matrix (real part)"):
    fig, ax = plt.subplots(figsize=(8, 6))
    real_part = np.real(dm.data)
    cax = ax.matshow(real_part, cmap='RdBu')#, vmin=-1, vmax=1)
    plt.title(title)
    plt.colorbar(cax)
    plt.show()

# Choose a noise level (temperature proxy)
T1, T2 = 5e-6, 4e-6  # "High temperature" setting

# Run everything
noise_model = create_thermal_noise_model(T1, T2)
qc = create_superposition_circuit()
dm = simulate_density_matrix(qc, noise_model)

# Display
print("Final Density Matrix (complex):\n", dm)
plot_density_matrix(dm, title="High Temp: Final Density Matrix (Re)")
