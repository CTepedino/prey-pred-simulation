package ar.edu.itba.ss.simulation;

public record SimulationParameters(
        double areaRadius,

        int initialPreyCount,
        double preyMinRadius,
        double preyMaxRadius,
        double preyLifeTime,
        double preyReproductionTime,
        double maxPreySpeed,

        int initialPredCount,
        double predMinRadius,
        double predMaxRadius,
        double predLifeTime,
        double predReproductionTime,
        double predHungerTime,
        double maxPredSpeed,

        double baseReproductionProbability,
        int maxCapacity,

        double dt,
        int dtsPerPrint,
        double maxTime,

        double beta,
        double tau,

        double A_pred, double B_pred,
        double A_prey, double B_prey,
        double A_wall, double B_wall
) {
    private static final double AREA_RADIUS = 15;
    private static final double R_MIN = 0.15;
    private static final double R_MAX = 0.35;
    private static final double V_MAX_PREY = 6;
    private static final int N_PREY = 70;

    private static final double LIFE_T_PREY = 10;
    private static final double REPRO_T_PREY = 1;

    private static final double P_0 = 0.3;
    private static final int N_CAP = 1000;

    private static final double DT = 0.0125;

    private static final double BETA = 1; //TODO
    private static final double TAU = .5; //TODO

    private static final double A_PRED = 8;
    private static final double B_PRED = 4;
    private static final double A_PREY = 4;
    private static final double B_PREY = 1;
    private static final double A_WALL = 8;
    private static final double B_WALL = 1;


    public static SimulationParameters ExperimentParams(double alpha, int N_pred, int dtsPerPrint, double maxTime){
        if (Double.compare(alpha, 0.8) < 0 || Double.compare(alpha, 1.2) > 0 || N_pred < 0 || N_pred > N_PREY){
            throw new IllegalArgumentException();
        }

        double v_max_pred = alpha * V_MAX_PREY;
        double life_t_prey = 4 * AREA_RADIUS / v_max_pred;
        double repro_t_prey = life_t_prey/10;
        double hunger_t_prey = life_t_prey/5;


        return new SimulationParameters(
                AREA_RADIUS,
                N_PREY, R_MIN, R_MAX, LIFE_T_PREY, REPRO_T_PREY, V_MAX_PREY,
                N_pred, R_MIN, R_MAX, life_t_prey, repro_t_prey, hunger_t_prey, v_max_pred,
                P_0, N_CAP,
                DT, dtsPerPrint, maxTime,
                BETA, TAU,
                A_PRED, B_PRED, A_PREY, B_PREY, A_WALL, B_WALL
        );
    }
}
