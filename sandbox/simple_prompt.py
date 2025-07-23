from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# Step 1: Define a simple concept graph
prompt_graph = {
    0: {0: "Scene: ancient ruins", 1: "Scene: neon city"},
    1: {0: "Style: monochrome",    1: "Style: vaporwave"},
    2: {0: "Mood: serene",         1: "Mood: chaotic"}
}

# Step 2: Build a graph state: 3 qubits connected linearly
def graph_state_circuit():
    qc = QuantumCircuit(3, 3)
    # Superposition
    for i in range(3):
        qc.h(i)
    # Entangle with CZ along edges (0-1 and 1-2)
    qc.cz(0, 1)
    qc.cz(1, 2)
    # Measure
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc

# Step 3: Execute and interpret
def run_prompt_engine():
    qc = graph_state_circuit()
    backend = Aer.get_backend('qasm_simulator')
    tqc = transpile(qc, backend)
    result = backend.run(tqc, shots=1).result()
    bitstring = list(result.get_counts().keys())[0]  # e.g., '101'

    # Interpret bitstring (reverse if needed)
    prompt_parts = []
    for i, bit in enumerate(reversed(bitstring)):
        prompt_parts.append(prompt_graph[i][int(bit)])

    final_prompt = ", ".join(prompt_parts)
    return final_prompt

# Generate a prompt
print("Quantum-Entangled Prompt:")
print(run_prompt_engine())
