import numpy as np

from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute


def deutsch_jozsa(marked_element):
    # Determine number of qubits needed
    N = len(f)
    n = int(np.log2(N))
    
    # Initialise n qubit register, classical readout register and ancilla qubit
    q = QuantumRegister(n, 'ctrl')
    c = ClassicalRegister(n, 'meas')
    a = QuantumRegister(n-1, 'anc')
    t = QuantumRegister(1, 'tgt')
    	
    # Combine resources into a quantum circuit
    qc = QuantumCircuit(q, a, t, c)
    
    # Step 1: Start with n qubit register in equal superposition
    for i in range(n):
        qc.h(q[i])
    	
    # Put the target ancilla qubit into the |-> state
    qc.x(t[0])
    qc.h(t[0])
    
    # Define n-qubit CNOT gate
    def MultiCNOT():
        # Compute
        qc.ccx(q[0], q[1], a[0])
        for i in range(2, n):
            qc.ccx(q[i], a[i-2], a[i-1])
        # Copy
        qc.cx(a[n-2], t[0])
        # Uncompute
        for i in range(n-1, 1, -1):
            qc.ccx(q[i], a[i-2], a[i-1])
        qc.ccx(q[0], q[1], a[0])
        
    # Apply oracle U_f which flips the phase of every state |x> with f(x) = 1
    for i in range(N):
        if f[i] == '1':   # Then we need to flip the phase
            state = bin(i)[2:].zfill(n)   
            for j in range(n):
                if state[j] == '0':
                    qc.x(q[j])
            MultiCNOT()
            for j in range(n):
                if state[j] == '0':
                    qc.x(q[j])
	
    # Apply Hadamards to working qubits
    for i in range(n):
        qc.h(q[i])
        
    # Measure our quantum register via our classical register
    for i in range(n):
        qc.measure(q[i], c[i])

    # Execute the quantum circuit on the local simulator
    job = execute(qc, 'local_qasm_simulator')
    result = job.result()
    print('If the results are all zero then the function is constant.')
    print('The results of the simulation shots are:', result.get_counts(qc))


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
