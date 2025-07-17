package ar.edu.itba.ss;

import ar.edu.itba.ss.simulation.Simulation;
import ar.edu.itba.ss.simulation.SimulationParameters;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Locale;

public class Main {

    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);

        Files.createDirectories(Paths.get("./results"));

        double[] alphas = new double[]{1.0};
        for(double alpha: alphas){
            int[] n_preds = new int[]{60};
            for(int n_pred: n_preds) {

                String outDir = String.format("./results/N=%d_a=%.2f", n_pred, alpha);
                Files.createDirectories(Paths.get(outDir));

                for (int i = 0; i < 5; i++) {

                    Simulation simulation = new Simulation(SimulationParameters.ExperimentParams(alpha, n_pred, 10, 10), outDir + "/" + i);
                    simulation.run();
                }

            }
        }
    }

}