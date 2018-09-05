using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;

namespace Quantum.Simple{

    class Driver{

        static void Main(string[] args){

            // Use the quantum simulator to check the outcomes of the quantum AND gate.
            System.Console.WriteLine("Qubit1 | Qubit2 | AND");
            using (var sim = new QuantumSimulator()){
                Result[] states = { Result.Zero, Result.One };
                foreach (Result input1 in states) {
                    foreach (Result input2 in states) {
                        Result output = testQAND.Run(sim, input1, input2).Result;
                        System.Console.WriteLine($"{input1}\t{input2}\t{output}");
                    }
                }
            }
            System.Console.WriteLine("Press any key to continue...");
            System.Console.ReadKey();
        }
    }
}