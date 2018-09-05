# Import the library
from qdk import *

# Create a quadratic polynmial  3x_2 + x_0x_1 - 2x_0x_2 - 2x_1x_2 
builder = QuadraticBinaryPolynomialBuilder() 
builder.add_term(3.0, 2, 2) 
builder.add_term(1.0, 0, 1) 
builder.add_term(-2.0, 0, 2)
builder.add_term(-2.0, 1, 2) 
qubo = builder.build_polynomial()

# Create a local solver 
solver = DWaveSolver()

# Get configuration of best solution 
solver.solver.num_reads = 300  # Sample 300 times
sol = solver.minimize(qubo)
print(sol) 