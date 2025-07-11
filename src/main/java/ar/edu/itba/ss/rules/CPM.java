package ar.edu.itba.ss.rules;

import ar.edu.itba.ss.model.Particle;
import ar.edu.itba.ss.model.Predator;
import ar.edu.itba.ss.model.Prey;
import ar.edu.itba.ss.model.Vector2D;
import ar.edu.itba.ss.simulation.SimulationParameters;
import ar.edu.itba.ss.simulation.SimulationState;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CPM implements Ruleset{

    @Override
    public SimulationState updateState(SimulationState state, SimulationParameters parameters) {
        SimulationState nextState = new SimulationState(state.time() + parameters.dt(), new ArrayList<>(), new ArrayList<>());

        for(Predator p: state.predators()){

            //1 -> determinar colisiones y target de particulas
            //2 -> ajustar radios segun colisiones
            //3 -> calcular v_d
            //4 -> actualizar v y x
            boolean inContact = false;
            Vector2D velocityUnitVector = null;

            for (Predator other: state.predators()) {
                if (p == other) continue;
                if (interacting(p, other)){
                    inContact = true;
                    velocityUnitVector = p.getPosition().subtract(other.getPosition()).normalize();
                    break;
                }
            }

            double wallDistance = parameters.areaRadius() - p.getPosition().magnitude();
            if (wallDistance <= p.getRadius()) {
                inContact = true;
                velocityUnitVector = p.getVelocity().scale(-1).normalize();
            }

            if (!inContact){
                Vector2D target = closest(p.getPosition(), state.preys());
                Vector2D e = target.subtract(p.getPosition()).normalize();


                double radius = Math.min(parameters.predMaxRadius(), p.getRadius() + parameters.predMaxRadius() * parameters.dt() / parameters.tau());
                double vMag = parameters.maxPredSpeed() *
                        Math.pow((p.getRadius() - parameters.predMinRadius())/(parameters.predMaxRadius() - parameters.predMinRadius()), parameters.beta());
                Vector2D velocity = e.scale(vMag);
                Vector2D position = p.getPosition().add(velocity.scale(parameters.dt()));

                nextState.predators().add((Predator) p.update(radius, velocity, position, parameters.dt()));

            } else {
                double radius = parameters.predMinRadius();
                double vMag = parameters.maxPredSpeed();
                Vector2D velocity = velocityUnitVector.scale(vMag);
                Vector2D position = p.getPosition().add(velocity.scale(parameters.dt()));


                nextState.predators().add((Predator) p.update(radius, velocity, position, parameters.dt()));
            }

        }

        for(Prey p: state.preys()){

        }

        return nextState;
    }


    private Vector2D closest(Vector2D current, List<? extends Particle> particles){
        Vector2D best = null;
        double bestDistance = Double.POSITIVE_INFINITY;

        for (Particle p: particles){
            Vector2D pos = p.getPosition();
            double distance = pos.distanceSq(current);

            if (distance < bestDistance) {
                bestDistance = distance;
                best = pos;
            }
        }

        return best;
    }

    private boolean interacting(Particle a, Particle b){
        return a.getPosition().distanceTo(b.getPosition()) < a.getRadius() + b.getRadius();
    }

}

