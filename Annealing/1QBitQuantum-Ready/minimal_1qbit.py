from qdk import *

# Create a quadratic polynmial  -x_0 - x_1 + 2x_0x_1  
builder = QuadraticBinaryPolynomialBuilder() 
builder.add_term(-1.0, 0, 0) 
builder.add_term(-1.0, 1, 1) 
builder.add_term(2.0, 1, 0)  
qubo = builder.build_polynomial()

# Create a local solver 
solver = DWaveSolver()

# Get configuration of best solution 
solver.solver.num_reads = 300 # Sample 300 times
sol = solver.minimize(qubo)
print(sol) 