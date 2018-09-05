# 1. Calling Libraries
from pyquil.quil  import Program 
from pyquil.api   import QVMConnection 
from pyquil.gates import X, CCNOT

# 2. Initialising the program
qvm = QVMConnection()
p = Program()

# 3. Applying gates
p.inst(X(0),X(1),X(2)) # so here 111
p.inst(CCNOT(0,1,2)) 

# 4. Performing measurements
p.measure(0,0)
p.measure(1,1)
p.measure(2,2)

# 5. Executing the program
results = qvm.run(p, [], 4)
print(results)