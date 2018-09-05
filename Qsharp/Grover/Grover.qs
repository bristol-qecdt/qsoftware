namespace Quantum.Grover{

    open Microsoft.Quantum.Primitive;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Extensions.Math; // to use maths functions
    open Microsoft.Quantum.Extensions.Convert; // to allow conversions between types


    /// # Summary
    /// Given an Int[] of marked elements it demonstrates Grover's search algorithm.
    /// # Input 
    /// ## size
    /// An integer, the size of the database to be searched
    /// # Output 
    /// Int: the element found to be the marked one by the algorithm
    operation Grover (size: Int) : (Int, Int) {
        
        body{
            // "size" is the number of elements in the database. "regLen" is the 
            // number of (qu)bits required to be able to represent all of them.
            let regLen =   Ceiling(Log(ToDouble(size))/Log(ToDouble(2)));  

            // Choose a value at random for the marked element and create an 
            // Int array representing the equivalent bit string (Little Endian).
            let markedVal = RandomInt(size);
            mutable markedValBits = new Int[regLen];
            mutable workingVal = markedVal;
            for (i in regLen-1..-1..0){
                set markedValBits[i] = workingVal/(2^(i));
                set workingVal = workingVal%(2^(i));
            }

            // Allocate all qubits required for the algorithm
            // The variable "outcome" must be declared outside the "using" block, 
            // as all variables in the block are local.
            mutable outcome = 0;
            using (qubits = Qubit[regLen+1]){

                // Separate main register and ancilla qubit
                let reg = qubits[0..regLen-1];
                let ancilla = qubits[regLen];
                
                // Apply Hadamard to each qubit in register
                ApplyToEach(H, reg);

                // Set ancilla qubit to |-> state
                X(ancilla);
                H(ancilla);

                // Loop U_f and D the required number of times
                let repetitions = Round(PI()/4.0*Sqrt(ToDouble(size))-0.5);
                for (i in 1..repetitions){
                    PhaseOracle(reg, ancilla, markedValBits);
                    D (reg, ancilla);
                }

                // Measure final state of register
                set outcome = MeasureInteger(LittleEndian(reg));

                // Clean all used qubits
                ResetAll(qubits);
            }

            return (outcome, markedVal);
        }
    }


    /// # Summary
    /// Implementation of U_f, which flips the phase when the main register is in the state |x>
    /// representing the marked element x.
    ///# Input 
    /// ## reg
    /// The Qubit[] representing the main register
    /// ## ancilla
    /// The ancilla Qubit
    /// ## markedElement: 
    /// The bit string as an Int[] representing the marked element x
    /// # Output 
    /// -
    operation PhaseOracle (reg: Qubit[], ancilla: Qubit, markedElement: Int[]) : () {

        body{
            // Apply X gate to all elements which are zero in the bit string
            for (i in 0..Length(markedElement)-1){
                if (markedElement[i] == 0){
                    X(reg[i]);
                }
            }

            // X gate on ancilla controlled on main register
            (Controlled X)(reg, (ancilla));

            // Reapply X gate to all elements which are zero in the bit string 
            // to return to original state.
            for (i in 0..Length(markedElement)-1){
                if (markedElement[i] == 0){
                    X(reg[i]);
                }
            }
        }

        adjoint auto
        controlled auto
        controlled adjoint auto
    }


    /// # Summary
    /// Implementation of the operation D in Grover's algorithm.
    ///# Input 
    /// ## reg
    /// The Qubit[] representing the main register
    /// ## ancilla
    /// The ancilla Qubit
    /// # Output 
    /// -
    operation D (reg: Qubit[], ancilla: Qubit) : (){
        
        body{
            // Apply Hadamard on all qubits in main register
            ApplyToEachCA(H, reg);

            // Apply U_0 
            ApplyToEachCA(X, reg);
            (Controlled X)(reg, (ancilla));
            ApplyToEachCA(X, reg);

            // Apply Hadamard on all qubits in main register
            ApplyToEachCA(H, reg);
        }

        adjoint auto
        controlled auto
        adjoint controlled auto
    }
}