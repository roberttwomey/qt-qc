from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# Step 1: Define your creative tree branches
tree = {
    0: {0: "Scene: Forest", 1: "Scene: City"},
    1: {0: "Style: Calm, Monochrome", 1: "Style: Vibrant, Kinetic"},
    2: {0: "Time: Dawn", 1: "Time: Midnight"}
}

# Step 2: Create 3-qubit quantum circuit (GHZ or Hadamard superposition)
qc = QuantumCircuit(3, 3)
qc.h([0, 1, 2])  # Independent randomness (change to GHZ for correlated)
qc.measure([0, 1, 2], [0, 1, 2])

# Step 3: Simulate and get bitstring
backend = Aer.get_backend('aer_simulator')
tqc = transpile(qc, backend)
result = backend.run(tqc, shots=1).result()
bitstring = list(result.get_counts().keys())[0]  # e.g., '101'
print("Bitstring:", bitstring)

# Step 4: Traverse the tree
description = []
for i, bit in enumerate(reversed(bitstring)):
    choice = tree[i][int(bit)]
    description.append(choice)

final_prompt = ", ".join(description)
print("Final Output:", final_prompt)
