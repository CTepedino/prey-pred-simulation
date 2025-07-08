package ar.edu.itba.ss.simulation;

import ar.edu.itba.ss.model.Predator;
import ar.edu.itba.ss.model.Prey;

import java.util.List;

public record SimulationState(
        double time,
        List<Predator> predators,
        List<Prey> preys
) {

}
