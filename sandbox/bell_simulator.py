from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Step 1: Create a quantum circuit with 2 qubits and 2 classical bits
qc = QuantumCircuit(2, 2)

# Step 2: Create superposition on qubit 0
qc.h(0)

# Step 3: Entangle qubit 0 and qubit 1 using a CNOT gate
qc.cx(0, 1)

# Step 4: Measure both qubits
qc.measure([0, 1], [0, 1])

# Step 5: Simulate the circuit using the qasm_simulator
backend = Aer.get_backend('aer_simulator')
tqc = transpile(qc, backend)
result = backend.run(tqc, shots=1000).result()
counts = result.get_counts()

# Step 6: Display the result
print("Measurement counts:", counts)
plot_histogram(counts)
plt.show()
