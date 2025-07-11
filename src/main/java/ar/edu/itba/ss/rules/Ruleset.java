package ar.edu.itba.ss.rules;

import ar.edu.itba.ss.simulation.SimulationParameters;
import ar.edu.itba.ss.simulation.SimulationState;

public interface Ruleset{

    SimulationState updateState(SimulationState state, SimulationParameters parameters);
}