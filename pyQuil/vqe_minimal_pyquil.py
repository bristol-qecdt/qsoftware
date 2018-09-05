# 1. Calling Libraries
from pyquil.quil import Program
from pyquil.api import QVMConnection
from pyquil.gates import RX
from pyquil.paulis import sZ,PauliSum,PauliTerm

# Calling Grove Library and optimiser
from grove.pyvqe.vqe import VQE 
import numpy as np
from scipy.optimize  import minimize

# 2. Initialising the program
qvm = QVMConnection()
vqe = VQE(minimizer=minimize, minimizer_kwargs={'method': 'nelder-mead'})

# 3. Defining ansatz
def ansatz(theta): 
    qp = Program()
    qp.inst(RX(theta[0],0))
    return qp
	
# 4. Defining Hamiltonian
hamiltonian = sZ(0) 

# 5. Running the VQE
initial_angle = [0.0]
result = vqe.vqe_run(ansatzv, hamiltonian, initial_angle, None, qvm=qvm) 
print(result)