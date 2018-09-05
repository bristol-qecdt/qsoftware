import dwave_qbsolv

# Create a quadratic polynomial -x_0 - x_1 + 2x_0x_1 
Q = {('x0', 'x0'): -1, ('x1', 'x1'): -1, ('x0', 'x1'): 2}

# Create the local solver
solver = dwave_qbsolv.QBSolv()

# Solve for the minimum energy configuration
response = solver.sample_qubo(Q, num_reads=300) # Sample 300 times
sol = list(response.samples())
energy = response.data_vectors['energy']
print(sol)
print(energy)