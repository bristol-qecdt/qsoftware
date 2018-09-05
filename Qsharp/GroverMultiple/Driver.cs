using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;

namespace Quantum.GroverMulti{

    class Driver{

        static void Main(string[] args){

            // Example of array of marked elements
            QArray<long> markedElements = new QArray<long>(20, 100, 40, 237, 65, 79, 101);
            long sizeOfDatabase = 500;

            // Use quantum simulator to run Grover's algorithm for multiple marked elements.
            long quantumOutcome;
            using (var sim = new QuantumSimulator()) {
                var result = GroverMulti.Run(sim, sizeOfDatabase, markedElements).Result;
                (quantumOutcome) = result;
            }

            System.Console.WriteLine("The marked elements were {0:d}.\nThe quantum algorithm found {1:d}", markedElements, quantumOutcome);
            System.Console.WriteLine("Press any key to continue...");
            System.Console.ReadKey();
        }
    }
}