namespace Quantum.Deutsch_Jozsa{

    open Microsoft.Quantum.Primitive;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Extensions.Math; // to use maths functions
    open Microsoft.Quantum.Extensions.Convert; // to allow conversions between types


    /// # Summary
    /// Given a balanced or constant function, the Deutsch-Jozsa algorithm
    /// determines which of the two it is. 
    /// # Input 
    /// ## f_x
    /// A Bool[] which represents a constant or balanced function f(x). 
    /// E.g. if f(3) = 0, then f_x[3] = True or if f(0) = 1, then f_x[0] = False
    /// # Output 
    /// String: "balanced" if f_x is balanced, "constant" if f_x is constant
    operation Deutsch_Jozsa (f_x: Bool[]) : (String) {
        
        body {
            let regLen =   Ceiling(Log(ToDouble(Length(f_x)))/Log(ToDouble(2)));

            mutable functionType = "constant";
            using (qubits = Qubit[regLen+1]){

                // Separate main register and ancilla qubit
                let register = qubits[0..regLen-1];
                let ancilla = qubits[regLen];
                
                // Start with main register in |0> state and ancilla in |1> state
                X(ancilla);

                // Apply Hadamards to all
                ApplyToEach(H, qubits);

                // Apply phase oracle
                PhaseOracle (register, ancilla, f_x);

                // Apply Hadamards to all registers in the main register
                ApplyToEach(H, register);

                // If all qubits are in zero state -> constant f_x
                // Otherwise: balanced f_x
                for (i in 0..regLen-1){
                    let outcome = M(register[i]);
                    if (outcome == One){
                        set functionType = "balanced";
                    }
                }

                ResetAll(qubits);
            }

            return functionType;
        }
    }


    /// # Summary
    /// Implementation of U_f representing f(x) as a quantum operator
    /// # Input 
    /// ## reg
    /// The Qubit[] representing the main register
    /// ## ancilla
    /// The ancilla Qubit
    /// ## f_x: 
    /// The Bool[] representation of the function f(x)
    /// # Output 
    /// -
    operation PhaseOracle (reg: Qubit[], ancilla: Qubit, f_x: Bool[]) : () {

        body{
            // Loop through all possible states and if a phase change 
            // is required on this state, apply it.
            for (i in 0..Length(f_x)-1){
                for (j in 0..Length(reg)-1){
                    if (i%(2^j)==0){
                        X(reg[j]);
                    }
                }

                // X gate on ancilla controlled on main register
                if (f_x[i]){
                    (Controlled X)(reg, (ancilla));
                }
            }
        }

        adjoint auto
        controlled auto
        controlled adjoint auto
    }    
}