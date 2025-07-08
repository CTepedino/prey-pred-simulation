package ar.edu.itba.ss.simulation;

import ar.edu.itba.ss.model.Particle;
import ar.edu.itba.ss.model.Predator;
import ar.edu.itba.ss.model.Prey;

import java.util.ArrayList;
import java.util.List;

public class Simulation {

    private final SimulationParameters parameters;

    private double time = 0;
    private final List<Predator> predators = new ArrayList<>();
    private final List<Prey> preys = new ArrayList<>();

    public Simulation(SimulationParameters parameters){
        this.parameters = parameters;
    }


}
