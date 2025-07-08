package ar.edu.itba.ss.model;

public class Prey extends Particle {
    
    public Prey(int id, Vector2D position, Vector2D velocity, double radius){
        super(id, Role.PREY, position, velocity, radius, 0, 0, 0);
    }
}
