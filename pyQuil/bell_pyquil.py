# 1. Calling Libraries
from pyquil.quil  import Program 
from pyquil.api   import QVMConnection 
from pyquil.gates import H, CNOT, X, Z

# 2. Initialising the program
qvm = QVMConnection()
p = Program()

# 3. Applying gates
p.inst(H(0),CNOT(0,1))            # |00> + |11>
#p.inst(H(0),CNOT(0,1),X(1))      # |01> + |10>
#p.inst(H(0),CNOT(0,1),Z(1))      # |00> - |11>
#p.inst(H(0),CNOT(0,1),X(1),Z(1)) # |01> - |10>

# 4. Performing measurements
p.measure(0,0)
p.measure(1,1)

# 5. Executing the program
results = qvm.run(p, [], 4)
print(results)