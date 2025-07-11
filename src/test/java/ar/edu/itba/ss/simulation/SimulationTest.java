package ar.edu.itba.ss.simulation;

import ar.edu.itba.ss.model.Predator;
import ar.edu.itba.ss.model.Prey;

import org.junit.Test;
import java.util.List;

import static org.junit.Assert.*;

public class SimulationTest {

    @Test
    public void particlesInsideAndNonOverlapping() {
        // Arrange
        double alpha = 1.0;
        int N_pred = 20;
        int dtsPerPrint = 10;

        SimulationParameters params = SimulationParameters.ExperimentParams(alpha, N_pred, dtsPerPrint, 10);
        Simulation simulation = new Simulation(params, "a");

        List<Prey> preys = simulation.getPreys();
        List<Predator> predators = simulation.getPredators();

        // Assert: correct counts
        assertEquals("Cantidad incorrecta de presas", params.initialPreyCount(), preys.size());
        assertEquals("Cantidad incorrecta de depredadores", params.initialPredCount(), predators.size());

        // Assert: dentro del área
        for (Prey p : preys) {
            double dist = p.getPosition().magnitude();
            assertTrue("Presa fuera del área", dist + p.getRadius() <= params.areaRadius());
        }
        for (Predator p : predators) {
            double dist = p.getPosition().magnitude();
            assertTrue("Depredador fuera del área", dist + p.getRadius() <= params.areaRadius());
        }

        // Assert: sin solapamiento entre presas
        for (int i = 0; i < preys.size(); i++) {
            for (int j = i + 1; j < preys.size(); j++) {
                double dist = preys.get(i).getPosition().distanceTo(preys.get(j).getPosition());
                double minDist = preys.get(i).getRadius() + preys.get(j).getRadius();
                assertTrue("Presas solapadas", dist > minDist);
            }
        }

        // Assert: sin solapamiento entre depredadores
        for (int i = 0; i < predators.size(); i++) {
            for (int j = i + 1; j < predators.size(); j++) {
                double dist = predators.get(i).getPosition().distanceTo(predators.get(j).getPosition());
                double minDist = predators.get(i).getRadius() + predators.get(j).getRadius();
                assertTrue("Depredadores solapados", dist > minDist);
            }
        }

        // Assert: sin solapamiento entre presas y depredadores
        for (Prey prey : preys) {
            for (Predator predator : predators) {
                double dist = prey.getPosition().distanceTo(predator.getPosition());
                double minDist = prey.getRadius() + predator.getRadius();
                assertTrue("Presa y depredador solapados", dist > minDist);
            }
        }
    }
}
