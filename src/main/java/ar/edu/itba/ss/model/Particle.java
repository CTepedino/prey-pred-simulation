package ar.edu.itba.ss.model;

import java.util.Objects;

public abstract class Particle {

    protected final int id;
    protected final Role role;
    protected Vector2D position;
    protected Vector2D velocity;
    protected double radius;

    protected double lifeTime;
    protected double hungerTime;
    protected double reproductionTime;

    protected LifeStatus status;

    public Particle(int id, Role role, Vector2D position, Vector2D velocity, double radius, double lifeTime, double hungerTime, double reproductionTime, LifeStatus status) {
        this.id = id;
        this.role = role;
        this.position = position;
        this.velocity = velocity;
        this.radius = radius;
        this.lifeTime = lifeTime;
        this.hungerTime = hungerTime;
        this.reproductionTime = reproductionTime;
        this.status = status;
    }

    public abstract Particle update(double radius, Vector2D velocity, Vector2D position, double dt);

    public int getId() {
        return id;
    }

    public Role getRole() {
        return role;
    }

    public Vector2D getPosition() {
        return position;
    }

    public Vector2D getVelocity() {
        return velocity;
    }

    public double getRadius() {
        return radius;
    }

    public double getLifeTime() {
        return lifeTime;
    }

    public double getHungerTime() {
        return hungerTime;
    }

    public double getReproductionTime() {
        return reproductionTime;
    }

    public LifeStatus getStatus() {
        return status;
    }

    public void setStatus(LifeStatus status){
        this.status = status;
    }

    public void resetReproductionTime(){
        this.reproductionTime = 0;
    }

    @Override
    public String toString() {
        return "Particle{" +
                "id=" + id +
                ", role=" + role +
                ", position=" + position +
                ", velocity=" + velocity +
                ", radius=" + radius +
                ", lifeTime=" + lifeTime +
                ", hungerTime=" + hungerTime +
                ", reproductionTime=" + reproductionTime +
                ", status=" + status +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Particle particle)) return false;
        return id == particle.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }
}