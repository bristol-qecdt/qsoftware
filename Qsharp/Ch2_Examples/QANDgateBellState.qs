namespace Quantum.Simple{

    open Microsoft.Quantum.Primitive;
    open Microsoft.Quantum.Canon;   

    /// # Summary
    /// Given two states to initialise qubits two, performs a quantum AND gate 
    /// and returns the measurement of the outcome.
    /// # Input 
    /// ## state1, state2
    /// Results, representing the basis state each input qubit should be set to.
    /// # Output 
    /// The outcome of measuring the output state of the AND gate.
    operation testQAND (state1: Result, state2: Result) : (Result){
        
        body{
            mutable outcome = Zero;
            using(qubits = Qubit[3]){
                // Set the input qubits into the required states
                if (state1 == One){
                    X(qubits[0]);
                }

                if (state2 == One){
                    X(qubits[1]);
                }

                // do the quantum AND gate
                CCNOT(qubits[0], qubits[1], qubits[2]);

                // Measure the outcome of the gate
                set outcome = M(qubits[2]);

                ResetAll(qubits);

            }

            return outcome;
        }
    }


    /// # Summary
    /// Wrapper space to demonstrate creation of Bell states.
    operation SetBellState ():(){

        body{
            using (qubits = Qubit[2]){
                // Create |00> + |11>
                H(qubits[0]);
                CNOT(qubits[0], qubits[1]);

                ResetAll(qubits);
            }

            using (qubits2 = Qubit[2]){
                // Create |00> - |11>
                H(qubits2[0]);
                Z(qubits2[0]);
                CNOT(qubits2[0], qubits2[1]);
                
                ResetAll(qubits2);
            }

            using (qubits3 = Qubit[2]){
                // Create |01> + |01>
                H(qubits3[0]);
                CNOT(qubits3[0], qubits3[1]);
                X(qubits3[1]);
                
                ResetAll(qubits3);
            }

            using (qubits4 = Qubit[2]){
                // Create |01> - |10>
                H(qubits4[0]);
                Z(qubits4[0]);
                CNOT(qubits4[0], qubits4[1]);
                X(qubits4[1]);

                ResetAll(qubits4);
            }
        }
    }

}
