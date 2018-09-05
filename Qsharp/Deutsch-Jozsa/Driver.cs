using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;

namespace Quantum.Deutsch_Jozsa{

    class Driver{

        static void Main(string[] args){

            // Example input f_x represented by Boolean array
            QArray<bool> inputFunction = new QArray<bool>(true, true, false, false, true, false, true, false);
            //QArray<bool> inputFunction = new QArray<bool>(true, true, true, true, true, true, true, true);
            //QArray<bool> inputFunction = new QArray<bool>(true, true, true, true, false, false, false, false);
            //QArray<bool> inputFunction = new QArray<bool>(false, false, false, false, false, false, false, false);

            // Use quantum simulator to run Deutsch-Jozsa algorithm and determine 
            // whether the function is constant or balanced.
            string quantumOutcome;
            using (var sim = new QuantumSimulator()) {
                var result = Deutsch_Jozsa.Run(sim, inputFunction).Result;
                (quantumOutcome) = result;
            }

            System.Console.WriteLine("The given function was was {0:d}. The quantum algorithm found this function is {1:d}", inputFunction, quantumOutcome);
            System.Console.WriteLine("Press any key to continue...");
            System.Console.ReadKey();
        }
    }
}