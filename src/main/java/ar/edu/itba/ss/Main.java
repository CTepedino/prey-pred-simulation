package ar.edu.itba.ss;

import java.util.Locale;

public class Main {

    public static void main(String[] args){
        Locale.setDefault(Locale.US);


        Simulation simulation = new Simulation(1, (double)1/33, 200, "out.txt");
        simulation.run();

    }

}