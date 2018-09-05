import numpy as np

from pyquil.quil import Program
from pyquil.api import QVMConnection 
from pyquil.gates import H


def deutsch_jozsa(f): 
    # Determine number of qubits needed
    N = len(f)
    n = int(np.log2(N))

    # Invoking and renaming
    qvm = QVMConnection()
    p = Program() 
    
    # Applying first round of n Hadamards
    for i in range(n):
        p.inst(H(i))
    
    # Defining the Oracle matrix
    U_f = np.eye(N)
    for i in range(N):
        if f[i] == '1':
            U_f[i][i] = -1   
    # Adding the Oracle matrix as a gate
    p.defgate("Uf", U_f)
    # Applying Oracle gate
    p.inst(("Uf",) + tuple(range(n)))
    
    # Applying second run of n Hadamards
    for i in range(n):
        p.inst(H(i))
        
    # Measure all the qubits and output result
    for i in range(n):
        p.measure(i,i)
        
    # Run the program
    classical_reg = list(range(n))
    results = qvm.run(p, classical_reg, 1) 
    
    y = 0
    for i in range(n):
        y = y + 2**i*int(results[0][i])
      
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