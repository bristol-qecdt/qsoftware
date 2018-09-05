# 1. Calling Libraries
from pyquil.quil  import Program 
from pyquil.api   import QVMConnection 
from pyquil.gates import H
# 2. Initialising the program
qvm = QVMConnection()
p = Program()
# 3. Applying gates
p.inst(H(0))
# 4. Performing measurements
p.measure(0,0)
# 5. Executing the program
results = qvm.run(p, [], 4)
print(results)