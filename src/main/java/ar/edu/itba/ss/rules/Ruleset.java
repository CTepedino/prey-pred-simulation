package ar.edu.itba.ss.rules;

import ar.edu.itba.ss.model.Particle;

import java.util.List;

public interface Ruleset {

    List<Particle> updateParticles(List<Particle> particles);
}