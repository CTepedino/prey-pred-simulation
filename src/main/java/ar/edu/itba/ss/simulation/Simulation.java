package ar.edu.itba.ss.simulation;

import ar.edu.itba.ss.OutputWriter;
import ar.edu.itba.ss.model.LifeStatus;
import ar.edu.itba.ss.model.Predator;
import ar.edu.itba.ss.model.Prey;
import ar.edu.itba.ss.model.Vector2D;
import ar.edu.itba.ss.rules.CPM;
import ar.edu.itba.ss.rules.Ruleset;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Simulation {

    private final Ruleset ruleset = new CPM();
    private final SimulationParameters parameters;

    private SimulationState state;
    private int nextId = 1;

    private final OutputWriter writer;

    public Simulation(SimulationParameters parameters, String outPath){
        this.parameters = parameters;

        writer = new OutputWriter(outPath);

        state = generateInitialParticles();

    }
    private SimulationState generateInitialParticles(){
        Random random = new Random();

        List<Prey> preys = new ArrayList<>();
        List<Predator> predators = new ArrayList<>();

        for(int i = 0; i < parameters.initialPreyCount(); i++){
            while (true){
                Vector2D position = Vector2D.fromPolar(
                        random.nextDouble(parameters.areaRadius() - 2 * parameters.preyMinRadius()),
                        random.nextDouble(2* Math.PI));
                if (preys.stream().noneMatch(p -> p.getPosition().distanceTo(position) <= p.getRadius() + parameters.preyMinRadius())){
                    preys.add(new Prey(
                            nextId++,
                            position,
                            new Vector2D(parameters.maxPreySpeed(), 0),
                            parameters.preyMinRadius()
                    ));
                    break;
                }
            }
        }

        for(int i = 0; i < parameters.initialPredCount(); i++){
            while (true){
                Vector2D position = Vector2D.fromPolar(
                        random.nextDouble(parameters.areaRadius() - 2 * parameters.predMinRadius()),
                        random.nextDouble(2* Math.PI));
                if (predators.stream().noneMatch(p -> p.getPosition().distanceTo(position) <= p.getRadius() + parameters.predMinRadius()) &&
                        preys.stream().noneMatch(p -> p.getPosition().distanceTo(position) <= p.getRadius() + parameters.predMinRadius())){
                    predators.add(new Predator(
                            nextId++,
                            position,
                            new Vector2D(parameters.maxPredSpeed(), 0),
                            parameters.predMinRadius()
                    ));
                    break;
                }
            }
        }

        return new SimulationState(0, predators, preys);
    }

    public void run(){
        int toNextPrint = 0;
        while (Double.compare(state.time(), parameters.maxTime()) <= 0){

            if (toNextPrint == 0){
                writer.printState(state);
            }

            state.preys().removeIf(p -> p.getStatus() != LifeStatus.ALIVE);
            state.predators().removeIf(p -> p.getStatus() != LifeStatus.ALIVE);

            state = ruleset.updateState(state, parameters);

            preyLoop:
            for (Prey prey: state.preys()){

                for (Predator pred: state.predators()){
                    if (prey.getPosition().distanceTo(pred.getPosition()) <= pred.getRadius() + prey.getRadius()){
                        prey.setStatus(LifeStatus.DEAD_EATEN);
                        pred.eat();
                        continue preyLoop;
                    }
                }

                if (prey.getLifeTime() >= parameters.preyLifeTime()){
                    prey.setStatus(LifeStatus.DEAD_AGE);
                }

            }

            for (Predator pred: state.predators()){

                if (pred.getHungerTime() >= parameters.predHungerTime()){
                    pred.setStatus(LifeStatus.DEAD_HUNGER);
                }

                if (pred.getLifeTime() >= parameters.predLifeTime()){
                    pred.setStatus(LifeStatus.DEAD_AGE);
                }
            }


            //TODO: chequear particulas a reproducir -> generarlas

            toNextPrint = (toNextPrint + 1) % parameters.dtsPerPrint();
        }


        writer.close();
    }




    public List<Prey> getPreys(){ return state.preys(); }
    public List<Predator> getPredators(){return state.predators();}

}
