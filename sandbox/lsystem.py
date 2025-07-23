from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import turtle
import random

# Quantum randomness function
def quantum_bitstring(num_qubits=3):
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))
    qc.measure(range(num_qubits), range(num_qubits))
    
    backend = Aer.get_backend('aer_simulator')
    tqc = transpile(qc, backend)
    result = backend.run(tqc, shots=1).result()
    counts = result.get_counts()
    bitstring = list(counts.keys())[0]
    return bitstring

# L-System with quantum rule selection
class QuantumLSystem:
    def __init__(self, axiom, rules, angle_choices):
        self.axiom = axiom
        self.rules = rules
        self.angle_choices = angle_choices
        self.current = axiom
        self.angle = 25  # default angle

    def generate(self, iterations):
        for _ in range(iterations):
            next_string = ""
            for ch in self.current:
                if ch in self.rules:
                    bitstring = quantum_bitstring()
                    choice_index = int(bitstring, 2) % len(self.rules[ch])
                    next_string += self.rules[ch][choice_index]
                else:
                    next_string += ch
            self.current = next_string
            
            # Use quantum randomness to vary the angle
            angle_bits = quantum_bitstring(2)
            self.angle = self.angle_choices[int(angle_bits, 2) % len(self.angle_choices)]

    def draw(self, length=5):
        stack = []
        turtle.speed(0)
        turtle.bgcolor('black')
        turtle.color('lime')
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

# Define rules (quantum randomness picks which to apply)
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
qls.generate(iterations=4)
qls.draw(length=10)
