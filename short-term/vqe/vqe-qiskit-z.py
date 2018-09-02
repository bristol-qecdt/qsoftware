#!/usr/bin/env python3
from qiskit_aqua import Operator, run_algorithm
from qiskit_aqua.input import get_input_instance
# Defines the dictionary of pauli operations
pauli_dict = {
  "paulis": [
    { "coeff": { "imag": 0.0, "real": 1.0 }, "label": "Z"}
  ]
}
algo_input = get_input_instance("EnergyInput")
algo_input.qubit_op = Operator.load_from_dict(pauli_dict)
params = {
  "algorithm": { "name": "VQE" },
  "optimizer": { "name": "SPSA" },
  "variational_form": { "name": "RY", "depth": 5 },
  "backend": { "name": "local_qasm_simulator" }
}
# Runs a local simulation in qasm to produce the energy result
result = run_algorithm(params, algo_input)

print("Energy: ", result["energy"])
