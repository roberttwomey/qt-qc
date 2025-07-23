from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# Each prompt node has 2 qubits → 4 options per node
prompt_graph = {
    0: ["Scene: forest", "Scene: temple", "Scene: neon city", "Scene: underwater cave"],
    1: ["Style: monochrome", "Style: digital paint", "Style: vaporwave", "Style: glitch noir"],
    2: ["Mood: serene", "Mood: anxious", "Mood: euphoric", "Mood: uncanny"]
}

def build_graph_state_multibit():
    qc = QuantumCircuit(6, 6)  # 2 qubits per node × 3 nodes

    # Step 1: Superpose all qubits
    for i in range(6):
        qc.h(i)

    # Step 2: Graph entanglement (entangle pairs to encode coherence)
    qc.cz(0, 2)
    qc.cz(2, 4)
    qc.cz(1, 3)
    qc.cz(3, 5)

    # Step 3: Measure all qubits
    qc.measure(range(6), range(6))
    return qc

def interpret_multi_qubit_prompt(bitstring):
    prompt_parts = []
    for node_idx in range(3):
        qubit_a = int(bitstring[2*node_idx + 1])  # MSB
        qubit_b = int(bitstring[2*node_idx])      # LSB
        value = (qubit_a << 1) | qubit_b          # Binary to int
        prompt_parts.append(prompt_graph[node_idx][value])
    return ", ".join(prompt_parts)

def run_quantum_prompt():
    qc = build_graph_state_multibit()
    backend = Aer.get_backend('aer_simulator')
    tqc = transpile(qc, backend)
    result = backend.run(tqc, shots=1).result()
    bitstring = list(result.get_counts().keys())[0]  # e.g. '010110'

    # Reverse bitstring for correct qubit order
    bitstring = bitstring[::-1]
    return interpret_multi_qubit_prompt(bitstring)

# Run it
print("Quantum-Coherent Prompt:")
print(run_quantum_prompt())
