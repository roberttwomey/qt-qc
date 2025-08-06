# Quantum Computing Sandbox

This repository contains various Python scripts demonstrating quantum computing concepts using Qiskit. Each script explores different aspects of quantum mechanics and computation.

## Sandbox Scripts

### Core Quantum Demonstrations

**[image-superpose.py](sandbox/image-superpose.py)** - Demonstrates quantum superposition by blending four images equally, then using quantum measurement to "collapse" to one specific image, creating an animated GIF showing the transition from superposition to classical state.

**[video-superpose.py](sandbox/video-superpose.py)** - Creates a real-time quantum video experience where four videos are blended in superposition, then quantum measurement determines which video to "collapse" to, with smooth transitions between states.

**[bell_simulator.py](sandbox/bell_simulator.py)** - Implements the Bell state (quantum entanglement) using Hadamard and CNOT gates, demonstrating quantum correlation between two qubits that cannot be explained classically.

**[unitary.py](sandbox/unitary.py)** - Visualizes unitary evolution of a single qubit on the Bloch sphere, showing how quantum states evolve continuously in the XZ plane and generating an animated GIF of the evolution.

### Quantum Randomness & Decision Making

**[bit_collapse.py](sandbox/bit_collapse.py)** - Uses quantum randomness to traverse a decision tree, demonstrating how quantum measurement can generate truly random choices for creative applications like scene generation.

**[simple_prompt.py](sandbox/simple_prompt.py)** - Creates quantum-entangled prompts by using graph states (entangled qubits) to generate coherent, correlated creative descriptions rather than independent random choices.

**[prompt_tree_qiskit.py](sandbox/prompt_tree_qiskit.py)** - Expands quantum prompt generation to use multiple qubits per decision node, allowing for more complex quantum-coherent creative outputs with 4 options per category.

### Quantum Art & Generative Systems

**[lsystem.py](sandbox/lsystem.py)** - Combines quantum randomness with L-systems to generate fractal-like structures, where quantum measurement determines rule selection and angle choices for organic, non-deterministic patterns.

**[lsystem_ibm.py](sandbox/lsystem_ibm.py)** - Similar to lsystem.py but uses IBM's fake backend to simulate real quantum hardware noise, demonstrating how quantum computers behave differently from perfect simulators.

### Noise & Decoherence Studies

**[temp-choice.py](sandbox/temp-choice.py)** - Studies how temperature affects quantum randomness by simulating different T1/T2 relaxation times, showing how environmental noise impacts quantum measurement outcomes.

**[temp-decoherence.py](sandbox/temp-decoherence.py)** - Demonstrates quantum decoherence by showing how thermal noise destroys quantum superposition, transitioning from quantum interference to classical behavior as temperature increases.

**[temp-decohere-density.py](sandbox/temp-decohere-density.py)** - Visualizes the density matrix evolution under thermal noise, showing how quantum coherence is lost through the real components of the density matrix.

### Hardware & Backend Testing

**[fake-backends.py](sandbox/fake-backends.py)** - Tests quantum circuit transpilation and execution on simulated IBM hardware, demonstrating how real quantum computers require circuit optimization and handle noise.

## Requirements

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Key Quantum Concepts Demonstrated

- **Superposition**: Multiple states existing simultaneously (image-superpose.py, video-superpose.py)
- **Measurement & Collapse**: Quantum randomness determining classical outcomes
- **Entanglement**: Correlated quantum states (bell_simulator.py, simple_prompt.py)
- **Unitary Evolution**: Continuous quantum state changes (unitary.py)
- **Decoherence**: Loss of quantum properties due to environment (temp-*.py files)
- **Quantum Randomness**: True randomness for creative applications
- **Hardware Simulation**: Realistic quantum computer behavior (fake-backends.py, lsystem_ibm.py)

