# Import the library
import dwave_qbsolv

# Create a quadratic polynomial  3x_2 + x_0x_1 - 2x_0x_2 - 2x_1x_2
Q = {('x2', 'x2'): 3, ('x0', 'x1'): 1, ('x0', 'x2'): -2, ('x1', 'x2'):-2}

# Create the local solver
solver = dwave_qbsolv.QBSolv()

# Solve for the minimum energy configuration
response = solver.sample_qubo(Q, num_reads=300) # Sample 300 times
sol = list(response.samples())
energy = response.data_vectors['energy']
print(sol)
print(energy)