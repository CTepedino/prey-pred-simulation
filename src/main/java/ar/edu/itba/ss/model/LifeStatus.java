package ar.edu.itba.ss.model;

public enum LifeStatus {
    ALIVE("ALIVE"),
    DEAD_AGE("DEAD_AGE"),
    DEAD_HUNGER("DEAD_HUNGER"),
    DEAD_EATEN("DEAD_EATEN");

    private final String death;

    LifeStatus(String death){
        this.death = death;
    }

    @Override
    public String toString(){
        return death;
    }
}
