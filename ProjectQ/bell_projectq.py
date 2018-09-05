from projectq import MainEngine
from projectq.ops import X, H, CNOT, Measure, All

# Set up the simulator 
engine = MainEngine()

# Allocate two qubits
bell_1 = engine.allocate_qureg(2)
# Create |00> + |11>
# Apply Hadamard gate to first qubit to create superposition
H | bell_1[0]
# Apply CNOT gate controlled on the first
CNOT | (bell_1[0], bell_1[1])

# Create |00> - |11>
bell_2 = engine.allocate_qureg(2)
X | bell_2[0]
H | bell_2[0]
CNOT | (bell_2[0], bell_2[1])

# Create |01> + |10>
bell_3 = engine.allocate_qureg(2)
H | bell_3[0]
CNOT | (bell_3[0], bell_3[1])
X | bell_3[1]

# Create |01> - |10>
bell_4 = engine.allocate_qureg(2)
X | bell_4[0]
H | bell_4[0]
CNOT | (bell_4[0], bell_4[1])
X | bell_4[1]