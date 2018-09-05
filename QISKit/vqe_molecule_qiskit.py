from qiskit_aqua import Operator, run_algorithm
from qiskit_aqua.input import get_input_instance

# Define the dictionary representing the Hamiltonian of the simulated system
# R = 0.5 is the distance between the atoms in the molecule
pauli_dict = {"paulis": [
   { "coeff": { "imag": 0.0, "real": -2.3275 }, "label": "II" },
   { "coeff": { "imag": 0.0, "real": -0.1570 }, "label": "IX" },
   { "coeff": { "imag": 0.0, "real": -1.5236 }, "label": "IZ" },
   { "coeff": { "imag": 0.0, "real": -0.1570 }, "label": "XI" },
   { "coeff": { "imag": 0.0, "real": 0.3309 }, "label": "XX" },
   { "coeff": { "imag": 0.0, "real": 0.1570 }, "label": "XZ" },
   { "coeff": { "imag": 0.0, "real": -1.5236 }, "label": "ZI" },
   { "coeff": { "imag": 0.0, "real": 0.1570 }, "label": "ZX" },
   { "coeff": { "imag": 0.0, "real": 0.1115 }, "label": "ZZ" }]}

# Create input variable that specifies we want the energy value
algo_input = get_input_instance("EnergyInput")

# Adds the Hamiltonian information to the input variable
algo_input.qubit_op = Operator.load_from_dict(pauli_dict)

# Defines the algorithm input in terms of the pauli dict and that we want the energy value
# Specifies the attributes of the algorithm that will be used to find the ground state energy
# algorithm: we will use the VQE
# optimiser: best choice for optimisation dependent on the simulated system
# variational_form: the ansatz or first guess at a solution
# depth: the complexity of the circuit used in the algorithm
# backend: the actual device the code will be run on
params = {
  "algorithm": { "name": "VQE" },
  "optimizer": { "name": "SPSA" },
  "variational_form": { "name": "RY", "depth": 5 },
  "backend": { "name": "local_qasm_simulator" }}

# Runs the VQE
result = run_algorithm(params, algo_input)

# Prints the final result for the groun state energy of the system
print(result["energy"])