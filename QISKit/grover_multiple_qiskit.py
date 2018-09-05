import numpy as np

from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute


def grover_multiple(marked_elements):
    # Determine the number of qubits needed
    M = len(marked_elements)
    n = len(max(marked_elements, key=len))
    N = 2**n
    
    # Flip bitstrings
    for i in range(M):
      marked_elements[i] = marked_elements[i][::-1]
	
    # Determine the number of times to iterate 
    T = int(round(np.pi*np.sqrt(N)/4 - 0.5)) 
    print('Number of iterations T =',T)
    
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
        
    # Define the oracle
    def U_f():
        for k in range(M):
            # Apply U_f for each marked string
            for j in range(len(marked_elements[k])):
                if marked_elements[k][j] == '0':
                    qc.x(q[j])
            MultiCNOT()
            for j in range(len(marked_elements[k])):
                if marked_elements[k][j] == '0':
                    qc.x(q[j])
                    
    # Define the gate D
    def D():
        # Apply H and X
        for j in range(n):
            qc.h(q[j])
            qc.x(q[j])
        MultiCNOT()
        # Apply X and H
        for j in range(n):
            qc.x(q[j])
            qc.h(q[j])
	
    # Step 2: Repeat applications of U_f and D
    for i in range(T):
        U_f()
        D()
	
    # Measure our quantum register via our classical register
    for i in range(n):
        qc.measure(q[i], c[i])

    # Execute the quantum circuit on the local simulator
    job = execute(qc, 'local_qasm_simulator')
    result = job.result()
    print('The results of the simulation shots are:', result.get_counts(qc))

# Define input type for def
str_input = []
stop = 0
while stop == 0:
    str_input = str_input + [input("Input a bit string to find: ")]
    add_more = input("Add another marked string? (y/n) ")
    if add_more in ['n','N']:
        stop = 1

print('')
grover_multiple(str_input)
