package ar.edu.itba.ss.model;

public enum Death {
    TIME("TIME"),
    HUNGER("HUNGER"),
    EATEN("EATEN");

    private final String death;

    Death(String death){
        this.death = death;
    }

    @Override
    public String toString(){
        return death;
    }
}
