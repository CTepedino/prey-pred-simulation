package ar.edu.itba.ss.model;

public enum Role {
    PRED("PRED"),
    PREY("PREY");

    private final String role;

    Role(String role){
        this.role = role;
    }

    @Override
    public String toString(){
        return role;
    }
}
