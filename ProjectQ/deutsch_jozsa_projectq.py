import numpy as np

from projectq import MainEngine
from projectq.ops import All, Measure, H, X
from projectq.meta import Control


def deutsch_jozsa(f): 
    # Determine number of qubits needed
    N = len(f)
    n = int(np.log2(N))
    
    # Check we can simulate on our local simulator
    if n > 28:   # 28 qubits = 4GB of RAM
        print('Number of qubits required =', n, 'which is too large to simulate.')
        return 0

    # Initialise qubits
    engine = MainEngine()
    qubits = engine.allocate_qureg(n)
    ancilla = engine.allocate_qubit()
    
    # Start with qubits in equal superposition and ancilla in |->
    All(H) | qubits
    X | ancilla
    H | ancilla
    
    # Apply oracle U_f which flips the phase of every state |x> with f(x) = 1
    for i in range(N):
        if f[i] == '1':   # Then we need to flip the phase
            state = bin(i)[2:].zfill(n)
            for j in range(n):
                if state[j] == '0':
                    X | qubits[j]
            with Control(engine, qubits):
                X | ancilla
            for j in range(n):
                if state[j] == '0':
                    X | qubits[j] 
    
    # Apply Hadamards to working qubits
    All(H) | qubits

    # Measure all the qubits and output result
    All(Measure) | qubits
    Measure | ancilla
    engine.flush()
    
    y = 0
    for i in range(n):
        y = y + 2**i*int(qubits[i])
      
    if y == 0:
        print('Function is constant.')
    else:
        print('Function is balanced.')
        

# Examples of constant and balanced functions to test
# Number of qubits to test with
n = 3

# Test on a constant function - the all zero function
f = '0' * 2**n
print('Testing constant function with f = {0}'.format(f))
deutsch_jozsa(f)

print('')

# Test on a balanced function - alternating zeros and ones
f = '01' * 2**(n-1)
print('Testing balanced function with f = {0}'.format(f))
deutsch_jozsa(f)

