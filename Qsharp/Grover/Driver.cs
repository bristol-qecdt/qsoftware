﻿using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;

namespace Quantum.Grover{

    class Driver{

        static void Main(string[] args){

            // Use quantum simulator to run Grover's algorithm.
            long quantumOutcome, markedElement;
            using (var sim = new QuantumSimulator()) {
                var result = Grover.Run(sim, 500).Result;
                (quantumOutcome, markedElement) = result;
            }

            System.Console.WriteLine("The randomly selected marked element was {0:d}. " +
                "The quantum algorithm found {1:d}", markedElement, quantumOutcome);
            System.Console.WriteLine("Press any key to continue...");
            System.Console.ReadKey();
        }
    }
}