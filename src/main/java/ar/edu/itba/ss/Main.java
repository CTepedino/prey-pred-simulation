package ar.edu.itba.ss;

import ar.edu.itba.ss.simulation.Simulation;
import ar.edu.itba.ss.simulation.SimulationParameters;

import java.util.Locale;

public class Main {

    public static void main(String[] args){
        Locale.setDefault(Locale.US);


       Simulation simulation = new Simulation(SimulationParameters.ExperimentParams(1, 10, 1, 100), "out.txt");
       simulation.run();

    }

}