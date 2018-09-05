# numpy and scipy libraries
import numpy as np
from scipy.optimize import minimize
# pyQuil Library
from pyquil.quil import Program
from pyquil.api import QVMConnection
from pyquil.gates import RY, CNOT
from pyquil.paulis import PauliSum, PauliTerm
# Grove Library
from grove.pyvqe.vqe import VQE

# Defining Hamiltonian
hamiltonian = PauliSum([
              PauliTerm.from_list([("I", 0),("I", 1)], coefficient=-3.8505),
              PauliTerm.from_list([("I", 0),("X", 1)], coefficient=-0.2288),
              PauliTerm.from_list([("I", 0),("Z", 1)], coefficient=-1.0466),
              PauliTerm.from_list([("X", 0),("I", 1)], coefficient=-0.2288),
              PauliTerm.from_list([("X", 0),("X", 1)], coefficient=0.2613),
              PauliTerm.from_list([("X", 0),("Z", 1)], coefficient=0.2288),
              PauliTerm.from_list([("Z", 0),("I", 1)], coefficient=-1.0466),
              PauliTerm.from_list([("Z", 0),("X", 1)], coefficient=0.2288),
              PauliTerm.from_list([("Z", 0),("Z", 1)], coefficient=0.2356)])
print(hamiltonian)

# Define ansatz
n_qubits = 2
depth = 3

def ansatz(params): 
    qp = Program()
    for i in range(depth):   
		qp.inst(CNOT(1,0))  
        for j in range(n_qubits):
            qp.inst(RY(params[j], j))  
    return qp

# Minimize and get approximate of the lowest eigenvalue
qvm = QVMConnection()
vqe = VQE(minimizer=minimize, minimizer_kwargs={'method': 'nelder-mead', 'options': {'xatol': 1.0e-2}})

# Initial Parameters
ip = np.random.uniform(0.0, 2*np.pi, size=n_qubits) 
result = vqe.vqe_run(ansatz, hamiltonian, ip, samples=None, qvm=qvm)
print(result)