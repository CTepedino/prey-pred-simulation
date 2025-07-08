package ar.edu.itba.ss;

import ar.edu.itba.ss.model.Particle;
import ar.edu.itba.ss.simulation.Simulation;
import ar.edu.itba.ss.simulation.SimulationState;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Locale;

public class OutputWriter {

    private final BufferedWriter writer;

    public OutputWriter(String outPath) {
        try {
            writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(outPath), StandardCharsets.UTF_8));
        } catch (IOException e){
            throw new RuntimeException(e);
        }
    }

    public void printState(SimulationState state){
        try {
            //TODO -> indicar muertas
            for (Particle particle : state.predators()) {
                writer.write(String.format(Locale.US, "%f %d %s %f %f %f %f %f %f %f %f ALIVE\n",
                        state.time(), particle.getId(), particle.getRole(),
                        particle.getPosition().x(), particle.getPosition().y(),
                        particle.getPosition().x(), particle.getVelocity().y(),
                        particle.getRadius(),
                        particle.getLifeTime(), particle.getReproductionTime(), particle.getHungerTime()

                ));
            }
            for (Particle particle : state.preys()) {
                writer.write(String.format(Locale.US, "%f %d %s %f %f %f %f %f %f %f 0 ALIVE\n",
                        state.time(), particle.getId(), particle.getRole(),
                        particle.getPosition().x(), particle.getPosition().y(),
                        particle.getPosition().x(), particle.getVelocity().y(),
                        particle.getRadius(),
                        particle.getLifeTime(), particle.getReproductionTime()
                ));
            }

        } catch (IOException e){
            throw new RuntimeException(e);
        }
    }

    public void close() {
        try {
            writer.close();
        } catch (IOException e){
            throw new RuntimeException();
        }
    }


}