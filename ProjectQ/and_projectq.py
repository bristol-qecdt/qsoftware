from projectq import MainEngine
from projectq.ops import X, Toffoli, All, Measure

# Set up the simulator 
engine = MainEngine()

print('Qubit1 | Qubit2 | Result')
for i in range(4):
    # Allocate qubits and ancilla
    qubits = engine.allocate_qureg(2)
    result = engine.allocate_qubit()
    # Set up all the input states
    if i == 1:
        # Input state 01
        X | qubits[0]
    elif i == 2:
        # Input state 10
        X | qubits[1]
    elif i == 3:
        # Input state 11
        X | qubits[0]
        X | qubits[1]
    # Apply the controlled-controlled NOT gate - this is called a Toffoli gate
    Toffoli | (qubits, result)
    # Measure the qubits
    All(Measure) | qubits
    Measure | result
    # Send the gates to the compiler/simulator
    engine.flush()
    print(int(qubits[0]),'\t', int(qubits[1]),'\t', int(result))