package ar.edu.itba.ss.simulation;

import ar.edu.itba.ss.OutputWriter;
import ar.edu.itba.ss.model.*;
import ar.edu.itba.ss.rules.CPM;
import ar.edu.itba.ss.rules.Ruleset;

import java.lang.reflect.Parameter;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Simulation {

    private final Ruleset ruleset = new CPM();
    private final SimulationParameters parameters;

    private int nextId = 1;

    private String outPath;

    Random random = new Random();


    public Simulation(SimulationParameters parameters, String outPath){
        this.parameters = parameters;
        this.outPath = outPath;
    }

    public void setSeed(int seed){
        random.setSeed(seed);
    }

    private SimulationState generateInitialParticles(){

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
        nextId = 1;
        SimulationState state = generateInitialParticles();
        OutputWriter writer = new OutputWriter(outPath);


        int toNextPrint = 0;
        while (Double.compare(state.time(), parameters.maxTime()) <= 0){

            if (toNextPrint == 0){
                writer.printState(state);
            }

            //Borro las que murieron despues de imprimir
            state.preys().removeIf(p -> p.getStatus() != LifeStatus.ALIVE);
            state.predators().removeIf(p -> p.getStatus() != LifeStatus.ALIVE);


            //Reproducción
            reproduction(state);

            //Actualizo targets/velocidades/posiciones
            state = ruleset.updateState(state, parameters);

            //Busco y dejo marcadas las muertes
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

            toNextPrint = (toNextPrint + 1) % parameters.dtsPerPrint();
        }


        writer.close();
    }


    private void reproduction(SimulationState state){
        List<Predator> predators = List.copyOf(state.predators());
        List<Prey> preys = List.copyOf(state.preys());


        for (Prey prey: preys){
            if (prey.getReproductionTime() >= parameters.preyReproductionTime()){
                double p_repro = Math.max(0, parameters.baseReproductionProbability() * (1 - ((double) state.preys().size() /parameters.maxCapacity())));
                if (random.nextDouble() < p_repro){
                    state.preys().add(new Prey(
                        nextId++,
                        prey.getPosition().add(Vector2D.fromPolar(prey.getRadius() + parameters.preyMinRadius(), random.nextDouble(2 * Math.PI))),
                        new Vector2D(parameters.maxPreySpeed(), 0),
                        parameters.preyMinRadius()
                    ));
                }

                prey.resetReproductionTime();
            }
        }

        for(Predator predator: predators){
            if (predator.getReproductionTime() >= parameters.predReproductionTime()){
                double p_repro = Math.max(0, parameters.baseReproductionProbability() * (1 - ((double) state.predators().size() /parameters.maxCapacity())));
                if (random.nextDouble() < p_repro){
                    state.predators().add(new Predator(
                        nextId++,
                        predator.getPosition().add(Vector2D.fromPolar(predator.getRadius() + parameters.predMinRadius(), random.nextDouble(2 * Math.PI))),
                        new Vector2D(parameters.maxPredSpeed(), 0),
                        parameters.predMinRadius()
                    ));
                }

                predator.resetReproductionTime();
            }

        }

    }

}
