import numpy as np

from projectq import MainEngine
from projectq.ops import All, Measure, H, X
from projectq.meta import Control


def grover_multiple(marked_elements): 
    # Determine number of qubits needed
    M = len(marked_elements)
    n = len(marked_elements[0])
    N = 2**n
    
    # Check we can simulate on our local simulator
    if n > 28:   # 28 qubits = 4GB of RAM
        print('Number of qubits required =', n, 'which is too large to simulate.')
        return 0
    
    # Determine number of times to iterate
    T = int(round(np.pi*np.sqrt(N/M)/4 - 0.5)) 
    print('Number of iterations T =',T)
    
    # Initialise qubits
    engine = MainEngine()
    qubits = engine.allocate_qureg(n)
    ancilla = engine.allocate_qubit()
    
    # Step 1: Start with qubits in equal superposition and ancilla in |->
    All(H) | qubits
    X | ancilla
    H | ancilla
    
    # Define the oracle
    def U_f():
        for k in range(M):
            # Apply U_f for each marked string
            for j in range(n):
                if marked_elements[k][j] == '0':
                    X | qubits[j]
            with Control(engine, qubits):
                X | ancilla
            for j in range(n):
                if marked_elements[k][j] == '0':
                    X | qubits[j]  
    
    # Define the gate D                
    def D():
        # Apply Hadamards
        All(H) | qubits
        # Apply U_0
        All(X) | qubits
        with Control(engine, qubits):
            X | ancilla
        All(X) | qubits
        # Apply Hadamards
        All(H) | qubits
    
    # Step 2: Repeat applications of U_f and D
    for i in range(T):
        U_f()
        D()

    # Step 3: Measure all the qubits and output result
    All(Measure) | qubits
    Measure | ancilla
    engine.flush()

    res = ''.join(str(int(qubit)) for qubit in qubits)
    
    print('Element found =', res)
    return res


str_input = []
stop = 0
while stop == 0:
    str_input = str_input + [input("Input a bit string to find: ")]
    add_more = input("Add another marked string? (y/n) ")
    if add_more in ['n','N']:
        stop = 1

print('')
grover_multiple(str_input) 