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
                if (target != null){
                    Vector2D e = target.subtract(p.getPosition()).normalize();


                    double radius = Math.min(parameters.predMaxRadius(), p.getRadius() + parameters.predMaxRadius() * parameters.dt() / parameters.tau());
                    double vMag = parameters.maxPredSpeed() *
                            Math.pow((p.getRadius() - parameters.predMinRadius())/(parameters.predMaxRadius() - parameters.predMinRadius()), parameters.beta());
                    Vector2D velocity = e.scale(vMag);
                    Vector2D position = p.getPosition().add(velocity.scale(parameters.dt()));

                    nextState.predators().add((Predator) p.update(radius, velocity, position, parameters.dt()));
                } else {
                    nextState.predators().add((Predator) p.update(p.getRadius(), p.getVelocity(), p.getPosition(), parameters.dt()));
                }
            } else {
                double radius = parameters.predMinRadius();
                double vMag = parameters.maxPredSpeed();
                Vector2D velocity = velocityUnitVector.scale(vMag);
                Vector2D position = p.getPosition().add(velocity.scale(parameters.dt()));


                nextState.predators().add((Predator) p.update(radius, velocity, position, parameters.dt()));
            }

        }

        for(Prey p: state.preys()){

            boolean inContact = false;
            Vector2D velocityUnitVector = null;

            for (Prey other: state.preys()) {
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
                Vector2D target = getPreyTarget(p, state, parameters);
                Vector2D e = target.subtract(p.getPosition()).normalize();


                double radius = Math.min(parameters.preyMaxRadius(), p.getRadius() + parameters.preyMaxRadius() * parameters.dt() / parameters.tau());
                double vMag = parameters.maxPreySpeed() *
                        Math.pow((p.getRadius() - parameters.preyMinRadius())/(parameters.preyMaxRadius() - parameters.preyMinRadius()), parameters.beta());
                Vector2D velocity = e.scale(vMag);
                Vector2D position = p.getPosition().add(velocity.scale(parameters.dt()));

                nextState.preys().add((Prey) p.update(radius, velocity, position, parameters.dt()));

            } else {
                double radius = parameters.preyMinRadius();
                double vMag = parameters.maxPreySpeed();
                Vector2D velocity = velocityUnitVector.scale(vMag);
                Vector2D position = p.getPosition().add(velocity.scale(parameters.dt()));


                nextState.preys().add((Prey) p.update(radius, velocity, position, parameters.dt()));
            }

        }

        return nextState;
    }


    private Vector2D closest(Vector2D current, List<? extends Particle> particles){
        Vector2D best = null; //Si no hay presas, se queda quieto
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

    private Vector2D getPreyTarget(Prey prey, SimulationState state, SimulationParameters parameters){
        Vector2D target = Vector2D.zero();

        for(Predator p: state.predators()){
            Vector2D e = prey.getPosition().subtract(p.getPosition()).normalize();
            double d = prey.getPosition().distanceTo(p.getPosition());
            Vector2D n = e.scale(parameters.A_pred()* Math.exp(-d/parameters.B_pred()));

            target = target.add(n);
        }

        for(Prey p: state.preys()){
            if (p == prey) continue;

            Vector2D e = prey.getPosition().subtract(p.getPosition()).normalize();
            double d = prey.getPosition().distanceTo(p.getPosition());
            Vector2D n = e.scale(parameters.A_prey()* Math.exp(-d/parameters.B_prey()));

            target = target.add(n);
        }

        Vector2D closestWallPoint = prey.getPosition().scale(parameters.areaRadius() / prey.getPosition().magnitude());
        Vector2D e = prey.getPosition().subtract(closestWallPoint).normalize();
        double d = prey.getPosition().distanceTo(closestWallPoint);
        Vector2D n = e.scale(parameters.A_wall()* Math.exp(-d/parameters.B_wall()));
        target = target.add(n);

        return target;
    }


}

