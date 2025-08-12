from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import json

# --- Circuit: 6 qubits -> [q0..q3]=zoom bits, [q4..q5]=video bits ---
def selection_circuit():
    qc = QuantumCircuit(6, 6)
    # Put all 6 qubits into uniform superposition
    for i in range(6):
        qc.h(i)
    # Measure 1:1 into classical bits
    qc.measure([0,1,2,3,4,5], [0,1,2,3,4,5])
    return qc

def sample_once(qc):
    """Run one shot and decode (zoom_raw 0..15, video 0..3)."""
    backend = Aer.get_backend('qasm_simulator')
    tqc = transpile(qc, backend)
    result = backend.run(tqc, shots=1).result()
    bitstring = list(result.get_counts().keys())[0]  # e.g., '100101'
    bits = list(reversed(bitstring))  # index i now corresponds to qubit i

    # zoom = bits q0..q3 (little-endian)
    zoom_raw = sum(int(bits[i]) << i for i in range(4))
    # video = bits q4..q5 (little-endian)
    video = sum(int(bits[4 + i]) << i for i in range(2))
    return zoom_raw, video

def sample_zoom_video():
    """Rejection-sample so zoom is uniform over 0..11."""
    qc = selection_circuit()
    while True:
        zoom_raw, video = sample_once(qc)
        if zoom_raw < 12:
            return {"zoom": zoom_raw, "video": video}
        # else: reject values 12..15 and resample

if __name__ == "__main__":
    selection = sample_zoom_video()
    print(json.dumps(selection))
