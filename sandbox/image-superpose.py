from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt

# === Step 1: Create Quantum Circuit ===
qc = QuantumCircuit(2, 2)
qc.h([0, 1])             # Put both qubits in superposition
qc.measure([0, 1], [0, 1])  # Measure into classical bits

# === Step 2: Simulate the circuit ===
backend = Aer.get_backend('qasm_simulator')
job = backend.run(qc, shots=1)  # 1 shot to simulate single collapse
result = job.result()
counts = result.get_counts()

# Get the single outcome (e.g. '10')
outcome = list(counts.keys())[0]
print("Measured:", outcome)

# === Step 3: Load and blend images ===
# Load 4 images corresponding to outcomes
paths = {
    "00": "image-00.jpg",
    "01": "image-01.jpg",
    "10": "image-10.jpg",
    "11": "image-11.jpg",
}

# Load images as PIL.Image
images = {k: Image.open(paths[k]).convert("RGBA") for k in paths}

# Create a blended superposition preview (equal weights)
blend = Image.blend(
    Image.blend(images["00"], images["01"], alpha=0.5),
    Image.blend(images["10"], images["11"], alpha=0.5),
    alpha=0.5
)

# === Step 4: Animate and export as GIF ===
frames = []
transition_steps = 30  # Number of frames for each transition
hold_frames = 30       # Hold each state for this many frames

for outcome in ["00", "01", "10", "11"]:
    # Hold the blend for a few frames
    for _ in range(hold_frames):
        frames.append(blend.copy())
    # Crossfade from blend to outcome image
    for i in range(transition_steps + 1):
        alpha = i / transition_steps
        frame = Image.blend(blend, images[outcome], alpha)
        frames.append(frame)
    # Hold the outcome image for a few frames
    for _ in range(hold_frames):
        frames.append(images[outcome].copy())

# Save as GIF
frames[0].save(
    "superposition_animation.gif",
    save_all=True,
    append_images=frames[1:],
    duration=100,  # ms per frame
    loop=0
)

print("GIF saved as superposition_animation.gif")

# === Step 4: Show the result ===
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].imshow(blend)
axs[0].set_title("Superposition Blend")
axs[0].axis("off")

axs[1].imshow(images[outcome])
axs[1].set_title(f"Collapsed State: {outcome}")
axs[1].axis("off")

plt.tight_layout()
plt.show()
