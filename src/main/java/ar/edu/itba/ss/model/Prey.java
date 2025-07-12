package ar.edu.itba.ss.model;

public class Prey extends Particle {
    
    public Prey(int id, Vector2D position, Vector2D velocity, double radius){
        super(id, Role.PREY, position, velocity, radius, 0, 0, 0, LifeStatus.ALIVE);
    }

    private Prey(int id, Vector2D position, Vector2D velocity, double radius, double lifeTime, double reproductionTime){
        this(id, position, velocity, radius);
        this.lifeTime = lifeTime;
        this.reproductionTime = reproductionTime;
    }

    @Override
    public Particle update(double radius, Vector2D velocity, Vector2D position, double dt) {
        return new Prey(id, position, velocity, radius, lifeTime + dt, reproductionTime + dt);
    }


}
