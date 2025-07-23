from qiskit_ibm_provider import IBMQ
from qiskit import QuantumCircuit, transpile, assemble
import turtle
import time

# Load IBMQ and get backend
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')  # adjust if you’re in a different hub
backend = provider.get_backend('ibmq_lima')  # or any available backend

# Generate quantum bitstring using real backend
def quantum_bitstring_real(num_qubits=3):
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))  # Put qubits in superposition
    qc.measure(range(num_qubits), range(num_qubits))

    transpiled = transpile(qc, backend)
    qobj = assemble(transpiled, shots=1)
    job = backend.run(qobj)
    result = job.result()
    counts = result.get_counts()
    bitstring = list(counts.keys())[0]
    return bitstring

# L-System class (same as before)
class QuantumLSystem:
    def __init__(self, axiom, rules, angle_choices):
        self.axiom = axiom
        self.rules = rules
        self.angle_choices = angle_choices
        self.current = axiom
        self.angle = 25

    def generate(self, iterations):
        for _ in range(iterations):
            next_string = ""
            for ch in self.current:
                if ch in self.rules:
                    bitstring = quantum_bitstring_real()
                    choice_index = int(bitstring, 2) % len(self.rules[ch])
                    next_string += self.rules[ch][choice_index]
                else:
                    next_string += ch
            self.current = next_string
            
            angle_bits = quantum_bitstring_real(2)
            self.angle = self.angle_choices[int(angle_bits, 2) % len(self.angle_choices)]

    def draw(self, length=5):
        stack = []
        turtle.speed(0)
        turtle.bgcolor('black')
        turtle.color('cyan')
        turtle.penup()
        turtle.goto(0, -250)
        turtle.setheading(90)
        turtle.pendown()
        
        for ch in self.current:
            if ch == 'F':
                turtle.forward(length)
            elif ch == '+':
                turtle.right(self.angle)
            elif ch == '-':
                turtle.left(self.angle)
            elif ch == '[':
                stack.append((turtle.pos(), turtle.heading()))
            elif ch == ']':
                pos, heading = stack.pop()
                turtle.penup()
                turtle.goto(pos)
                turtle.setheading(heading)
                turtle.pendown()
        turtle.done()

# Define quantum L-system with rules
rules = {
    'F': [
        "F[+F]F[-F]F",
        "F[-F]F",
        "F[+F]F",
        "FF"
    ]
}

angle_choices = [20, 25, 30, 35]

qls = QuantumLSystem(axiom="F", rules=rules, angle_choices=angle_choices)
qls.generate(iterations=3)
qls.draw(length=7)
