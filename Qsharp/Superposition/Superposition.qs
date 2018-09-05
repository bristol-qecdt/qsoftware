namespace Quantum.Superposition{

    open Microsoft.Quantum.Primitive;
    open Microsoft.Quantum.Canon;

    /// # Summary
    /// Creates an equal superposition state |0> + |1> 
    /// and measures it in the computational basis.
    /// # Input 
    /// -
    /// # Output 
    /// Result: the outcome of the measurement of the superposition
    operation Superposition() : (Result){

        body{
            // Variable to be returned must be declared outside using block
            mutable res = Zero;

            // Create a qubit reqister
            using (reg = Qubit[1]){

                // Apply the Hadamard gate to your qubit to create an equal superposition
                H(reg[0]);

                // Measure the qubit in superposition
                set res = M(reg[0]);

                // Reset the qubit to its clean |0> state
                Reset(reg[0]);
            }

            return res;
        }
    }
}
