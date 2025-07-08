package ar.edu.itba.ss.model;

public class Predator extends Particle {

    public Predator(int id, Vector2D position, Vector2D velocity, double radius){
        super(id, Role.PRED, position, velocity, radius, 0, 0, 0);
    }
}
