package ar.edu.itba.ss.model;

public class Predator extends Particle {

    public Predator(int id, Vector2D position, Vector2D velocity, double radius){
        super(id, Role.PRED, position, velocity, radius, 0, 0, 0, LifeStatus.ALIVE);
    }

    private Predator(int id, Vector2D position, Vector2D velocity, double radius, double lifeTime, double hungerTime, double reproductionTime){
        this(id, position, velocity, radius);
        this.lifeTime = lifeTime;
        this.hungerTime = hungerTime;
        this.reproductionTime = reproductionTime;
    }

    @Override
    public Particle update(double radius, Vector2D velocity, Vector2D position, double dt) {
        return new Predator(id, position, velocity, radius, lifeTime + dt, hungerTime + dt, reproductionTime + dt);
    }

    public void eat(){
        hungerTime = 0;
    }
}
