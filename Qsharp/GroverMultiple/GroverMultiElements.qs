namespace Quantum.GroverMulti{

    open Microsoft.Quantum.Primitive;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Extensions.Math; // to use maths functions
    open Microsoft.Quantum.Extensions.Convert; // to allow conversions between types

    newtype BitString = (Int[]);


    /// # Summary
    /// Given an Int[] of marked elements it demonstrates Grover's search algorithm
    /// for multiple marked elements.
    /// # Input 
    /// ## size
    /// An integer, the size of the database to be searched
    /// ## markedElements
    /// An Int[] representing the marked elements in the database, 
    /// the phase of which is flipped by U_f
    /// # Output 
    /// Int: the element found to be a marked one by the algorithm
    operation GroverMulti (size: Int, markedElements: Int[]) : (Int) {
        
        body{
            // "size" is the number of elements in the database. "regLen" is the 
            // number of (qu)bits required to be able to represent all of them.
            let regLen =   Ceiling(Log(ToDouble(size))/Log(ToDouble(2)));  

            // Create Int arrays representing the equivalent bit strings (Little Endian) 
            // of the marked elements passed to this operation.
            let numMarkedElements = Length(markedElements);
            mutable markedValBits = new BitString[numMarkedElements];
            mutable workingVal = 0;
            for (i in 0..numMarkedElements-1){
                mutable bitString = new Int[regLen];
                let markedVal = markedElements[i];
                set workingVal = markedVal;
                for (j in regLen-1..-1..0){
                    set bitString[j] = workingVal/(2^(j));
                    set workingVal = workingVal%(2^(j));
                }
                set markedValBits[i] = BitString(bitString);
            }
            
            // Allocate all qubits required for the algorithm
            // The variable "outcome" must be declared outside the "using" block, 
            // as all variables in the block are local.
            mutable outcome = 0;
            using (qubits = Qubit[regLen+1]){

                // Separate main register and ancilla qubit
                let reg = qubits[0..regLen-1]
                let ancilla = qubits[regLen]
                
                // Apply Hadamard to each qubit in register
                ApplyToEach(H, reg);

                // Set ancilla qubit to |-> state
                X(ancilla[0]);
                H(ancilla[0]);

                // Loop U_f and D the required number of times
                let repetitions = Round(PI()/4.0*Sqrt(ToDouble(size)/ToDouble(numMarkedElements))-0.5);
                for (i in 1..repetitions){
                    PhaseOracle(reg, ancilla, markedValBits);
                    D (reg, ancilla);
                }

                // Measure final state of register and clean all qubits
                set outcome = MeasureInteger(LittleEndian(reg));
                ResetAll(qubits);
            }

            return (outcome);
        }
    }


    /// # Summary
    /// Implementation of U_f representing f(x) as a quantum operator
    /// # Input 
    /// ## reg
    /// The Qubit[] representing the main register
    /// ## ancilla
    /// The ancilla Qubit
    /// ## markedElements: 
    /// The BitString[] representing all the marked elements. 
    /// BitString is a user defined wrapper type for an Int[].
    /// # Output 
    /// -
    operation PhaseOracle (reg: Qubit[], ancilla: Qubit, markedElements: BitString[]) : () {

        body{
            // Loop through all marked elements
            for (i in 0..Length(markedElements)-1){
                // Apply X gate to all qubits which are zero in the bit string
                for (j in 0..Length(markedElements[i])-1){
                    if (markedElements[i][j] == 0){
                        X(reg[j]);
                    }
                }

                // X gate on ancilla controlled on main register
                (Controlled X)(reg, (ancilla));

                // Reapply X gate to all elements which are zero in the bit string 
                // to return to original state.
                for (j in 0..Length(markedElements[i])-1){
                    if (markedElements[i][j] == 0){
                        X(reg[j]);
                    }
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